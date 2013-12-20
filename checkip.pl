#!/usr/bin/perl
$IP_FILE = "ipemail.result";
my $localip= `/sbin/ifconfig | grep "inet addr" | grep -v 127.0.0.1`;
my $newip = `/usr/bin/wget http://ifconfig.me/ip -O - -q`;
my $hostname = `hostname`;
my $oldip = getoldip();
my $send_to = "To: you\@you.com\n";
my $reply_to = "Reply-to: you\@you.com\n";
my $from = "From: you\@you.com\n";
my $subject = "Subject: IP Address: $newip\n";
my $content = "$hostname\n $newip\n $localip";
chomp($newip);
if($newip ne $oldip)
{
print "old ip >$oldip<\n";
writenewip($newip);
unless(open (MAIL, "|/usr/sbin/sendmail you\@you.com"))
{
print "error.\n";
warn "Error starting sendmail: $!";
}
else{
print MAIL $from;
print MAIL $reply_to;
print MAIL $subject;
print MAIL $send_to;
print MAIL "Content-type: text/html\n\n";
print MAIL $content;
close(MAIL) || warn "Error closing mail: $!";
print "Mail sent\n";
}
}

sub writenewip
{
my($newip) = @_;
print ("new IP = >$newip<\n");
open IPFILE, ">$IP_FILE";
print IPFILE "$newip";
close IPFILE;
}

sub getoldip
{
open IPFILE, "$IP_FILE";
my($line) = 0;
while ( <IPFILE> )
{
$line = $_;
chomp($line);
}
close IPFILE;
return($line);
}

