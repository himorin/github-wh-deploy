#! /usr/bin/perl

use strict;
use lib '../';

use Encode;
use JSON;
use Cwd;

use PNAPI::Constants;
use PNAPI::Config;
use PNAPI::CGI;

my $obj_cgi = new PNAPI::CGI;
my $obj_config = new PNAPI::Config;

# if not POST, do nothing and return
if ($obj_cgi->request_method() ne 'POST') {
  $obj_cgi->send_error(503, 'Not POST');
  exit;
}

my $postdata = $obj_cgi->param('POSTDATA');
utf8::encode($postdata);
my $cdat = decode_json($postdata);

# for temporal debug and develop purpose
my $r_hash = $ENV{'HTTP_X_GITHUB_DELIVERY'};
$r_hash = PNAPI::Constants::LOCATIONS()->{'config'} . '/ghwh/' . $r_hash;
open(FILE, ">$r_hash.json");
print FILE $postdata;
close(FILE);

if ($ENV{'X-GitHub-Event'} ne 'push') {
  print $obj_cgi->header();
  print "{\"response\": \"ok\"}";
}

# extract commit information
my $gc = {};
$gc->{'ref'} = $cdat->{'ref'};
my @ctmp = split(/\//, $cdat->{'ref'});
$gc->{'branch'} = $ctmp[-1];
$gc->{'name'} = $cdat->{'repository'}->{'full_name'};
$gc->{'updated'} = $cdat->{'repository'}->{'updated_at'};
$gc->{'pushed'} = $cdat->{'repository'}->{'pushed_at'};
$gc->{'hash_before'} = $cdat->{'before'};
$gc->{'hash_after'} = $cdat->{'after'};

# match with config - for DB, just query by SELECT
foreach (@{$obj_config->get('targets')}) {
  if (($_->{'repo'} eq $gc->{'name'}) && ($_->{'branch'} eq $gc->{'branch'})) {
    # git command - XXX find better solution?
    my $c_cwd = getcwd();
    chdir $_->{'target'};
    my $p_git_out;
    open(P_GIT, "git pull |");
    while (readline(P_GIT)) { $p_git_out .= $_ . "\n"; }
    close(P_GIT);
    chdir $c_cwd;
    open(FILE, ">$r_hash.out");
    print FILE $p_git_out;
    close(FILE);
  }
  last;
}

print $obj_cgi->header();
print "{\"response\": \"ok\"}";

exit;
