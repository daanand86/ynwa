#!/usr/bin/perl
use strict;
use warnings;
use POSIX qw(strftime);
use Data::Dumper;
use IPC::Run qw(run timeout);
use lib '/data01/home/svmso/vdi/lib';
use MDG::VDI      qw( :VDI );
use MDG::ThreePar qw( :VDI );

print "Starting the load_THREEPAR_ACTIVITY.pl script...\n";

my ($in, $out, $err);

# Grab the date so we can label the output file with it
my $fileDate = strftime "%F_%T", localtime;
my $outCSV = "/data01/home/svmso/vdi/THREEPAR_ACTIVITY_$fileDate.csv";
open (OUTPUT, ">", $outCSV);

#my @threePars = getDbThreeParList('noignore');
my @threePars = getDbThreeParList('all');

foreach my $threePar (@threePars) {
    printf("%-37s","Processing 3Par $threePar... ");

    # Execute the "statvlun" command against the 3Par and capture the output to an array
    #my @output = qx( /usr/bin/ssh $threePar "statvlun -vvsum -iter 1 -d 60" 2>&1  );
    my @sshCmd  = ('/usr/bin/ssh', $threePar, 'statvlun','-vvsum', '-iter', '1', '-d', '60');
    eval {
        run \@sshCmd,  \$in , \$out, \$err, timeout(120, exception=>'timeout');
    };

    if ($@ =~ /timeout/) {
        print "  Timed out on 'statvlun' command...\n";
        next;
    }
    my @output = split /\n/, $out;

    # Did we receive enough lines of output from the command?
    if (scalar @output < 5) {
        # Nope... 
        print "  !!! Insufficient output !!!\n";
        #print Dumper \@output;
        next;   # ...so carry on.
    }
    # We did get enough output, so process the statvlun results
    my $errors = 0;
    foreach my $vlun (@output) {
        my $date = strftime "%F %T", localtime;
        if ($vlun =~ m/^(.*)\st\s*(\d+)\s*(\d+)\s*(\d+)\s*-*(\d+)\s*-*(\d+)\s*-*(\d+)/) {
           my $lunName = $1;
           my @iops = ($2,$3,$4);
           my @kbps = ($5,$6,$7);
           $lunName =~ s/\s//g;
           $lunName = uc($lunName);
           print OUTPUT "$date\t$threePar\t$lunName\t$iops[0]\t$iops[1]\t$iops[2]\t$kbps[0]\t$kbps[1]\t$kbps[2]\n";;
        }
        else {
           $errors++;
        }
    }
    print "  Error count = $errors\n";
}

# Close the out file
close OUTPUT;

my $mysqlDBH = initMysql();
my $mysqlLoad = "LOAD DATA LOCAL INFILE '$outCSV'
                 INTO TABLE THREEPAR_ACTIVITY
                 fields terminated by '\\t' ";
my $final = $mysqlDBH->prepare( $mysqlLoad );
$final->execute or die "SQL Error: $DBI::errstr\n";


##############################################################################
#  Clear out any records older than 90 days
##############################################################################
$mysqlDBH->do(q|DELETE FROM THREEPAR_ACTIVITY WHERE date < DATE_SUB(NOW(), INTERVAL 90 DAY)|);


##############################################################################
#  Wait for MySQL to close the file so we can delete it
##############################################################################
while ( `/usr/sbin/lsof | grep $outCSV` ) {
   sleep(2);
}

unlink $outCSV;

$mysqlDBH->disconnect;

print "Finished the load_THREEPAR_ACTIVITY.pl script.\n";

exit;
