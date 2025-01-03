#! /usr/bin/perl

use strict;
use lib '../';

use Encode;
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
my $cdat = decode_json $postdata;

# for temporal debug and develop purpose
my $hash = $ENV{'HTTP_X_GITHUB_DELIVERY'};
$hash = PNAPI::Constants::LOCATIONS()->{'config'} . '/ghwh/' . $hash . '.json';
open(FILE, ">$hash");
print FILE $postdata;
close(FILE);

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
foreach (@{$obj_config->{'targets'}}) {
  if (($_->{'repo'} eq $gc->{'name'}) && ($_->{'branch'} eq $gc->{'branch'})) {
    # git command - XXX find better solution?
    my $c_cwd = getcwd();
    chdir $_->{'target'};
    chdir $c_cwd;
  }
  last;
}

print $obj_cgi->header();
print "{\"response\": \"ok\"}";

exit;
