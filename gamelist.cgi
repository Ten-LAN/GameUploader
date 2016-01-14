#!/usr/bin/perl --

# This program Encode Shift-JIS !!!!!!!!!!

use strict;
use warnings;

# Program
our $GAMEDIR = './Game';
our $SETTING = 'data.ini';
our $SSFILE  = 'ss.png';

our %GET = &DecodeGet( exists( $ENV{ 'QUERY_STRING' } ) ? $ENV{ 'QUERY_STRING' } : '' );
our %ARG = &Arg( %GET );

my $json = &JsonOut();
print "Content-type:text/html; charset=shift_jis\n";
print "Content-length: " . length( $json ) . "\n";
print "Content-Disposition: attachment; filename=\"gamelist.json\"\n";
print "\n";
print $json;

sub Arg()
{
  my ( %cgi ) = ( @_ );
  my %ret;

  $ret{ 'key' } = {};
  if ( $cgi{ 'getvalue' } ne '' )
  {
    my @list = split( /\,/, $cgi{ 'getvalue' } );
    foreach ( @list ) { $ret{ 'key' }{ $_ } = ''; }
  }
  return %ret;
}

sub JsonOut()
{
  my $json = '';
  my $max = 0;

  if ( opendir( DIR, $GAMEDIR ) )
  {
    my @list = &GetGameList( readdir( DIR ) );
    closedir( DIR );
    $max = scalar( @list );
    $json .= join( ',', @list );
  }

  return '{"max":"' . $max . '","gamelist":[' . $json . ']}';
}

sub JsonOutGameInfo()
{
  my ( %info ) = ( @_ );
  my @json;
  if ( scalar ( keys( %{ $ARG{ 'key' } } ) ) > 0 )
  {
    # Only key.

    foreach ( keys( %info ) )
    {
      if ( $_ ne 'catelist' && exists ( $ARG{ 'key' }{ $_ } ) )
      {
        push( @json, sprintf( '"%s":"%s"', $_, $info{ $_ } ) );
      }
    }

  } else
  {
    # Default.

    foreach ( keys( %info ) )
    {
      if ( $_ ne 'catelist' )
      {
        push( @json, sprintf( '"%s":"%s"', $_, $info{ $_ } ) );
      }
    }

  }

  return '{' . join( ',', @json ) . '}';
}

sub GetGameList()
{
  my ( @list ) = ( @_ );
  my @ret;

  foreach ( @list )
  {
    if ( $_ =~ /^([0-9]+)/ && -d $GAMEDIR . '/' . $_ )
    {
      my %info = &GetGameInfo( $_ );

      push( @ret, &JsonOutGameInfo( %info ) );

    }
  } # end foreach

  return @ret;
}

sub GetGameInfo()
{
  my ( $dir ) = ( @_ );
  my %ret;

  $ret{ 'number' } = -1;
  $ret{ 'catelist' }{ '-1' } = 'sub';

  if ( open( FILE, $GAMEDIR . '/' . $dir . '/' . $SETTING ) )
  {
    while( <FILE> )
    {
      #chomp( $_ );
      $_ =~ s/\r|\n//g; 
      my ( $key, $value ) = split( /\=/, $_, 2 );
      if ( $key eq 'cate' )
      {
        $ret{ $key } = $value;
        my ( $main, @clist ) = split( /\,/, $value );
        $ret{ 'catelist' }{ $main } = 'main';
        foreach ( @clist )
        {
          $ret{ 'catelist' }{ $_ } = 'sub';
        }
      } elsif ( $key ne '' )
      {
        $ret{ $key } = $value;
      }
    }
    close( FILE );

    # Get game number.
    $dir =~ /^([0-9]+)/;
    $ret{ 'number' } = $1;
  }

  return %ret;
}

sub DecodeGet()
{
  my ( $query ) = ( @_, '' );
  my %ret;
  $ret{ 'game' } = 0;
  $ret{ 'getvalue' } = '';

  my @args = split( /&/, $query );
  foreach ( @args )
  {
    my ( $name, $val ) = split( /=/, $_, 2 );
    $val =~ tr/+/ /;
    $val =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack('C', hex($1))/eg;
    $ret{ $name } = $val;
  }

  return %ret;
}
