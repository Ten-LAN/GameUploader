#!/usr/bin/perl

package count;

use strict;
use warnings;

our $LOGFILE = './log.txt';

my $out = &Main();

print "Content-type:text/html\n";
print "Content-length: " . length( $out ) . "\n";
print "\n";
print $out;

sub Main()
{
  my $time = time();
  my $ipaddr = exists( $ENV{ 'REMOTE_ADDR' } ) ? $ENV{ 'REMOTE_ADDR' } : 'UNKNOWN';
  my $number = exists( $ENV{ 'QUERY_STRING' } ) ? $ENV{ 'QUERY_STRING' } : '';

  if ( $number ne '' && !($number =~ /[^ 0-9\&]/) )
  {
    my $playtime;
    ( $number, $playtime ) = split( /\&/, $number );
    return &Logging( $time, $ipaddr, $number, $playtime );
  }

  return &Out();
}

sub Logging()
{
  my ( $time, $ipaddr, $number, $playtime ) = ( @_ );

  if ( open ( FILE, "+>> $LOGFILE") )
  {
    flock( FILE, 2 );
    print FILE "$time\t$number\t$playtime\t$ipaddr\t\n";
    close( FILE );
    return '{"msg":"OK","game":"' . $number . '","playtime":"' . $playtime . '"}';
  }

  return '{"msg":"ERROR"}';
}

sub Out()
{
  require 'output.pl';
  return &GameLanking( $LOGFILE );
}
