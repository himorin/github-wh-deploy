#! /usr/bin/perl

use strict;
use lib './';

use JSON;
use Encode;

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




print $cgi->header();
print "{\"response\": \"ok\"}";

exit;
