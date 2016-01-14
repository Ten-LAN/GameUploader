#!/usr/bin/perl

use strict;
use warnings;

sub GameLanking()
{
  my ( $file ) = ( @_ );

  my $html = '';

  $html .= '<!DOCTYPE html>
<html lang="ja">
 <head>
 <meta charset="utf-8">
  <title>Ranking</title>
 </head>
 <body>
  <table>
';

  if ( open( FILE, "< $file" ) )
  {
    my @list = <FILE>;
    close( FILE );
    @list = &Analysis( @list );

    my $rank = 0;
    foreach ( @list )
    {
      $html .= sprintf( '   <tr><td>%d</td><td>%d</td><td>%d</td></tr>', ++$rank, $_{ 'number' }, $_{ 'count' } ) . "\n";
    }

  }

  $html .= '
  </table>
 </body>
</hmtl>
';

  return $html;
}

sub Analysis()
{
  my ( @list ) = ( @_ );
  my %data;

  my $get = exists( $ENV{ 'QUERY_STRING' } ) ? $ENV{ 'QUERY_STRING' } : '';

  foreach ( @list )
  {
    my ( $time, $number, $ipaddr ) = split( /\t/, $_ );

    if ( exists( $data{ $time } ) )
    {
      ++$data{ $time }{ 'count' };
      push( @{ $data{ $time }{ 'times' } }, $time );
    } else
    {
      $data{ $time }{ 'count' } = 1;
      $data{ $time }{ 'times' } = [ $time ];
    }
  }

  my @key = sort{ $data{ $a }{ 'count' } <=> $data{ $b }{ 'count' } }( keys( %data ) );
  my @ret;

  foreach ( @key )
  {
    push ( @key, { 'number' => $_, 'count'=> $data{ $_ }, 'times' => @{ $data{ $_ }{ 'times' } } } );
  }

  return @ret;
}

1;
