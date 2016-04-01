#!/usr/bin/perl --

# This program Encode Shift-JIS !!!!!!!!!!

use strict;
use warnings;
use Archive::Zip;
use CGI;

# Settings

our @CATEGORY       = ( 'アクション', 'シューティング', 'スポーツ', 'レース',  'パズル',  'テーブル', 'シミュレーション', 'ロールプレイング', '多人数',    'ミニゲーム', 'その他' );
our @CATEGORY_COLOR = ( '#ff0091',    '#ff2828',        '#dbae00',  '#c2cb10', '#16f000', '#00a411',  '#008f9a',          '#004eff',          '#cf00ff', '#f400ff',    '#808080' );

# Program

our $query = new CGI;
our %cgi;

# Exe path.
$cgi{ 'exe'     }  = $query->param( 'exe' ) ? $query->param( 'exe' ) : '';
# Game title.
$cgi{ 'title'   }  = $query->param( 'title' ) ? $query->param( 'title' ) : '';
# Game comment.
$cgi{ 'text'    }  = $query->param( 'text' )  ? $query->param( 'text' )  : '';
# Enable pad2key.
$cgi{ 'pad2key' }  = $query->param( 'pad2key' )  ? $query->param( 'pad2key' )  : '0';
# Is dvd.
$cgi{ 'dvd' }  = $query->param( 'dvd' )  ? '1'  : '0';

# Main category.
my $maincate   = $query->param( 'maincate' ) ? $query->param( 'maincate' ) : 0;
$maincate      = $maincate ? $maincate  : ( $maincate eq '0' ? 0 : scalar( @CATEGORY ) );
# Sub categorys.
my @subcate        = $query->param( 'subcate' );

# Create category.
@{ $cgi{ 'category' } } = ();
push ( @{ $cgi{ 'category' } }, $maincate );
if ( scalar( @subcate ) > 0 )
{
  my %cate;
  foreach ( @subcate ){ if ( $_ != $maincate ) { $cate{ $_ } = 0; } }

  push ( @{ $cgi{ 'category' } }, sort{ $a <=> $b }( keys( %cate ) ) );
}

# Idname( [ID]_[Idname] ).
$cgi{ 'idname'  }  = $query->param( 'idname' )  ? $query->param( 'idname' )  : '';
$cgi{ 'idname'  } =~ s/ //g;
$cgi{ 'idname'  } =~ s/[^ \d\w\_\-\+\=\(\)\[\]]//g;

# Upload game.
$cgi{ 'file'    }  = $query->param( 'file' )  ? $query->param( 'file' )  : '';

# Upload screen shot.
$cgi{ 'image'   }  = $query->param( 'image' ) ? $query->param( 'image' ) : '';
$cgi{ 'imagenum'   }  = $query->param( 'imagenum' ) ? $query->param( 'imagenum' ) : '';
$cgi{ 'page'    }  = $query->param( 'page' ) ? $query->param( 'page' ) : '';
$cgi{ 'page'    }  = $cgi{ 'page' } =~ /[^ \d]/ || $cgi{ 'page' } eq '' ? 0 : $query->param( 'number' );
# Game number.
$cgi{ 'number'  }  = $query->param( 'number' ) ? $query->param( 'number' ) : '';
if( defined( $query->param( 'number' ) ) && ! $query->param( 'number' )){ $cgi{ 'number' } = 0; }
$cgi{ 'number'  }  = ($cgi{ 'number' } =~ /[^ \d]/ || $cgi{ 'number' } eq '') ? -2 : $cgi{ 'number' };
#
$cgi{ 'content' }  = $query->param( 'content' ) ? $query->param( 'content' ) : '';


#if( $query->param( 'file' )  eq '' && $cgi{ 'title'   } eq '' && $cgi{ 'text'    } eq '' && $cgi{ 'image'   }  ne '' )
#{
#  
#}

if( $cgi{ 'number' } =~ /[^\d]/ )
{
  $cgi{ 'number' } = -1;
}

our $CgiScript = 'index.cgi';
our $GAMEDIR = './Game';
our $TEMPZIP = 'tmp.zip';
our $TEMPDIR = './tmp';
our $SETTING = 'data.ini';
our $SSFILE  = 'ss.png';
our $NOIMAGE = 'noimage.png';
our $PAGEV   = 10;

print &main();

sub main()
{
  my $html = '';

  my $up = $cgi{ 'number' } > -2 ? 0 : -1;
  if( $cgi{ 'title' } ne '' && $cgi{ 'text'  } ne '' )
  {
    $up = &Upload();
    return sprintf( 'Location:%s', $CgiScript . $up ) . "\n\n";
  }

  $html .= "Content-type:text/html; charset=shift_jis\n\n";

  $html .= &HtmlHeader();
  if( $cgi{ 'content' } eq 'howto' )
  {
    #HOWTO
    $html .= &HtmlHowTo();
  }elsif( $cgi{ 'content' } eq 'download' )
  {
    #DOWNLOAD
    $html .= &HtmlDownLoad();
  } elsif( $cgi{ 'content' } eq 'admin' )
  {
    # ADMIN
    my $sync = $query->param( 'sync' ) ? $query->param( 'sync' ) : '0';
    if ( $sync eq '1' )
    {
      # 同期処理！！！
    }

    $html .= &HtmlAdmin();
    $html .= &HtmlGameList();
  }else
  {
    #アップローダー
    $html .= &HtmlForm();
    $html .= &HtmlError( $up );
    $html .= &HtmlInformation();
    $html .= &HtmlMain();
    if ( &SearchGameDir( $cgi{ 'number' } ) eq '' )
    {
      $html .= &HtmlGameList();
    }
  }
  $html .= &HtmlFooter();

  return $html;
}

sub HtmlHowTo()
{
  my $html = '';

  $html.= sprintf('
  <div class="main">
   <div class="text">
    <h1>Ten-LAN GameUploader</h1>
    <h2>ここは？</h2>
    <p>ここはTen-LAN用のゲームアップローダーです。</p>
    <p>ここにアップするとTen-LAN GameDownloaderにてTen-LANにインストールすることが可能です。</p>
    <h2>使い方</h2>
    <h3>新規</h3>
    <p>アップローダーに入ってすぐの状態は新規アップロードとなります。操作は共通を見てください。</p>
    <h3>バージョンアップ</h3>
    <p>アップローダー下部のゲーム一覧からバージョンアップするゲームを探し、編集をクリックしてください。ゲームの個別ページに行けます。その後は共通の作業となります。</p>
    <h3>共通</h3>
    <p>ゲームタイトル、一言説明、カテゴリ、ZIPで圧縮したゲームデータ一式、PNG形式のスクリーンショットを入力し、アップロードしてください。</p>
    <p>PNGのスクリーンショットは必ずしも必要ではありませんが、ランチャーがさみしくなります。PNGでない場合動作は保証しません。また、大きすぎる画像は正常にテクスチャとして読み込めません。SSは3枚程度に収め、それ以上説明が必要ならゲーム内でチュートリアルを用意した方が良いでしょう。</p>
    <p>ゲーム名と一言説明は必ず入力してください。</p>
    <h4>カテゴリについて</h4>
    <p>カテゴリはメインカテゴリとサブカテゴリがあります。<input type="radio" checked="checked" />で選んだものはメインカテゴリで、1つしか選べません。ランチャーによってはメインの色分けに使われる場合もあります。<input type="checkbox" checked="checked" />で選択したものはサブカテゴリで、複数選ぶことが可能です。カテゴリ検索はメインサブ関係なくヒットします。</p>
    <h4>パッドキー変換</h4>
    <p>パッドキー変換とは、パッドの入力をキー入力に変換する機構を有効にするかどうかの設定です。これを有効にすると以下のようにゲームパッドのボタンがキーボード入力に変換されます。そのため個々のゲームでキーコンフィグを搭載したり、設定をする手間を削減できます(ただしアナログ入力が扱えないなど、いくつか制限がある)。</p>
    <p>また、複数人対戦やパッドキー変換とパッド入力の両対応をすると、挙動がおかしくなるので、パッドキー変換を使うか、自前でパッド入力を実装するかどちらかを選択してください。</p>
    <div style="text-align: center;"><img src="pad.png" /></div>
    <p>なお、このキーコンフィグはTen-LANにて行ったものを自動的に反映します。Z、Xキーに割り当てているパットのボタンはTen-LANでの決定やキャンセルのキーとなるので、ゲームの決定などをこれに合わせておくとユーザーフレンドリーになるでしょう。</p>
    <h3>アップロードの確認</h3>
    <p>ゲームの個別ページでは過去のバージョン一覧が見れます。ここでどのバージョンがいつアップロードされ、サイズはいくつなのかが分かります。ダウンロードして確認を行うこともできますが、ディレクトリは再構築されています。</p>
    <h2>詳細</h2>
    <h3>アップロード後の作業</h3>
    <p>アップロードされたZIPは解凍され、設定ファイルとスクリーンショットを入れた上で、適切にディレクトリ構造を作った後に再圧縮されます。</p>
    <p>ゲームごとに別の識別番号が割り当てられ、その専用ディレクトリ内に今までアップした全てのバージョンのデータが保存されます。</p>
    <p>Ten-LAN本体は一番新しいバージョンをダウンロードしインストールしますが、古いバージョンのゲームは削除しません。ハイスコアなどを回収したい場合は展示後各PCから回収してください。</p>
    <p>ゲームタイトルや一言は最新のみ反映され、過去のものは無視されます。ただしZIP圧縮されているため、過去のバージョンをダウンロードして解凍すれば確認できます。これはスクリーンショットも同様です。</p>
    <h3>設定ファイル</h3>
    <p>再圧縮されたZIPのGame/ゲーム番号/の下に、スクリーンショットと設定ファイルが設置されます。</p>
    <p>ZIP再圧縮の際に実行ファイル(*.exe)を検索しますが、その際複数あるとどれが選ばれるか分かりません。</p>
    <p>アップロード後、専用ページにてexeのパスを修正可能なので、そのような場合には手動で直してください。</p>
   </div>
');
  return $html;
}

sub HtmlDownLoad()
{
  my $html = '';

  $html.= sprintf('
  <div class="main">
   <div class="text">
    <h1>Download</h1>
    <h2>Ten-LAN</h2>
    <p>Ten-LAN本体とゲームインストーラーです。</p>
    <p class="download"><a href="./Ten-LAN.zip">- Download -</a></p>
    <h2>ゲームリスト(JSON)</h2>
    <p>Ten-LANに読み込ませるJSONです。</p>
    <p class="download"><a href="./gamelist.cgi">- Download -</a></p>
   </div>
');
  return $html;
}

sub HtmlAdmin()
{
  my $html = '';
  $html .= sprintf('
  <div class="text">
   <div style="text-align:center;"><div style="font-size:2em;color:red;">WARNING!!</div><p>分かる人以外触らないこと！！</p></div>
   <h1>システム管理</h1>
   <p class="download"><a href="%s?content=admin&sync=1">- 同期開始 -</a></p>
   <h1>ゲーム管理</h1>
  </div>
');
}

sub HtmlHeader()
{
  my $html = sprintf('<!DOCTYPE html>
<html lang="ja">
 <head>
 <meta charset="utf-8">
  <title>Ten-LAN Game Uploader</title>
  <link rel="stylesheet" href="./style.css">
  <meta name="author" content="Hiroki" />
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Cache-Control" content="no-cache">
  <meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT">
 </head>
<body>

  <div class="main">
  <header>
   <div class="menu">
    <div class="home"><a href="%s"></a></div>
    <div class="howto"><a href="%s?content=howto"></a></div>
    <div class="download"><a href="%s?content=download"></a></div>
    <div class="admin"><a href="%s?content=admin"></a></div>
   </div>
  </header>
',
  $CgiScript, $CgiScript, $CgiScript, $CgiScript );
  return $html;
}

sub HtmlFooter()
{
  my $html = sprintf('
  <div style="height:30px;width:800px;"></div>
  <footer>- Ten-LAN Game Uploader -</footer>
  </div>
 </body>
</html>
');
  return $html;
}

sub HtmlForm()
{
  my $html = '';
  my $uploader = '';
  my %form;
  $form{ 'title' } = $form{ 'text' } = '';
  $form{ 'number' } = -1;
  $form{ 'idname' } = '';
  $form{ 'imagenum' } = 1;

  my $checked_dvd = ' checked="checked"';
  my $checked = ' checked="checked"';
  my $maincate = scalar( @CATEGORY ) - 1;

  my $i;
  my @cate;
  for ( $i = 0 ; $i < scalar( @CATEGORY ) ; ++$i ){ push( @cate, '' ); }

  if ( $cgi{ 'number' } >= 0 )
  {
    my %data = &GetGameSetting( $cgi{ 'number' } );
    $form{ 'number' } = $cgi{ 'number' };
    $form{ 'title' }  = $data{ 'title' };
    $form{ 'text' }   = $data{ 'text' };
    $form{ 'idname' } = $data{ 'idname' };
    $form{ 'first' }  = $data{ 'first' };
    $form{ 'exe' }    = $data{ 'exe' };
    $form{ 'imagenum' }    = $data{ 'imagenum' };
    if( $data{ 'dvd' } == 0 ){ $checked_dvd = ''; }
    if( $data{ 'pad2key' } == 0 ){ $checked = ''; }
    my @catelist = split( /,/, $data{ 'cate' } );
    $maincate = shift( @catelist );
    foreach( @catelist ){ $cate[ $_ ] = ' checked="checked"'; }
    $form{ 'ver' } = $data{ 'ver' };
    $form{ 'gver' } = $data{ 'gver' };
    $form{ 'button' } = 'Updata';
    $uploader = 'ゲームのアップデート';
  } else
  {
    $form{ 'title' } = '新しいゲームの名前(既存のゲームは下の一覧へ)';
    $form{ 'button' } = 'Upload';
    $form{ 'exe' }    = '';
    $uploader = '新規ゲームアップロード';
  }
  $html .= sprintf( '   <div class="uploader">%s', "\n" );
  $html .= sprintf( '    <form action="%s" method="post" enctype="multipart/form-data">%s', $CgiScript, "\n" );
  $html .= sprintf( '     <table>%s', "\n" );
  $html .= sprintf( '      <caption>%s</caption>%s', $uploader, "\n" );
  $html .= sprintf( '      <colgroup class="left"></colgroup>%s', "\n" );
  $html .= sprintf( '      <colgroup class="right"></colgroup>%s', "\n" );
  $html .= sprintf( '      <tfoot>%s', "\n" );
  $html .= sprintf( '       <tr><td colspan="2"><input type="hidden" name="number" value="%d" /><input type="submit" value="%s" /></td></tr>%s', $form{ 'number' }, $form{ 'button' }, "\n" );
  $html .= sprintf( '      </tfoot>%s', "\n" );
  $html .= sprintf( '      <tr><td>ゲームタイトル</td><td><input type="text" name="title" value="%s" class="textinput" /></td></tr>%s', $form{ 'title' }, "\n" );
  $html .= sprintf( '      <tr><td>一言</td><td><input type="text" name="text" value="%s" class="textinput" /></td></tr>%s', $form{ 'text' }, "\n" );
  $html .= sprintf( '      <tr><td>カテゴリ<div><input type="radio" checked="checked">メインカテゴリ</div><div><input type="checkbox" checked="checked">サブカテゴリ</div></td><td>' );
  for ( $i = 0 ; $i < scalar( @CATEGORY ) ; ++$i )
  {
    $html .= sprintf( '<div class="cate" style="background-color:%s;"><input type="radio" name="maincate" value="%d"%s /><input type="checkbox" name="subcate" value="%d"%s />%s</div>', $CATEGORY_COLOR[ $i ], $i, $i == $maincate ? ' checked="checked"' : '',$i, $cate[ $i ], $CATEGORY[ $i ] );
  }
  $html .= sprintf( '<div style="clear:both;"></div></td></tr>%s', "\n" );
  $html .= sprintf( '      <tr><td>ゲーム(ZIP)</td><td><input type="file" name="file" /></td></tr>%s', "\n" );
  $html .= sprintf( '      <tr><td>スクリーンショット(PNG)</td><td><input type="file" name="image" /><br><input type="text" name="imagenum" value="%d" />枚(半角数字)</td></tr>%s', $form{ 'imagenum' }, "\n" );
  if( $cgi{ 'number' } >= 0 )
  {
    $html .= sprintf( '      <tr><td>実行ファイルパス</td><td><input type="text" name="exe" value="%s" />※分かる人以外触らない</td></tr>%s', $form{ 'exe' }, "\n" );
    $html .= sprintf( '      <tr><td>識別名</td><td><input type="hidden" name="idname" value="%s" />%s</td></tr>%s', $form{ 'idname' }, $form{ 'idname' }, "\n" );
    $html .= sprintf( '      <tr><td>公開年度</td><td>%.4s</tr>%s', $form{ 'first' }, "\n" );
    $html .= sprintf( '      <tr><td>バージョン</td><td>設定:%d / ゲーム:%d</td></tr>%s', $form{ 'ver' }, $form{ 'gver' }, "\n" );
  } else
  {
    $html .= sprintf( '      <tr><td>識別名</td><td><input type="text" name="idname" value="%s" /><br />半角英数のみ。設定すると少し嬉しい。</td></tr>%s', $form{ 'idname' }, "\n" );
  }
  $html .= sprintf( '      <tr><td>DVD収録</td><td><input type="checkbox" name="dvd" value="1" %s /></td></tr>%s', $checked_dvd, "\n" );
  $html .= sprintf( '      <tr><td>パッドキー変換有効</td><td><input type="checkbox" name="pad2key" value="1" %s /></td></tr>%s', $checked, "\n" );
  $html .= sprintf( '     </table>
    </form>
   </div>%s', "\n" );
  return $html;
}

sub HtmlError()
{
  my( $num ) = @_;
  my $html;
  if( $num == 0 )
  {
    $html = sprintf( '' );
  }
  return $html;
}

sub HtmlInformation()
{
  my $html = '';

  #my $dir = sprintf( '%s/%04d', $GAMEDIR, $cgi{ 'number' } );

  my $dir = &SearchGameDir( $cgi{ 'number' } );

  if ( $dir ne '' )#if( -d $dir )
  {
    $dir = sprintf ( '%s/%s', $GAMEDIR, $dir );

    opendir( DIR, $dir );
    my @list = readdir( DIR );
    closedir( DIR );

    my @version;
    foreach( @list )
    {
      if( $_ =~ /([0-9]+)\.zip/ )
      {
        push( @version, $1 );
      }
    }

    @version = sort{ $b <=> $a } @version;

    $html .= sprintf( '   <div class="version">' );
    $html .= sprintf( '    <a href="%s/%s" target="_blank"><img src="%s/%s" style="width:80px;height:60px;" /></a>', $dir, $SSFILE, $dir, $SSFILE );
#    $html .= sprintf( '    <div style="padding:5px auto;"><a href="%s/%s" target="_blank"><div style="background-image:url(%s/%s);background-size:80px;width:80px;height:60px;"></div></a></div>', $dir, $SSFILE, $dir, $SSFILE );
    $html .= sprintf( '    <table>' );
    $html .= sprintf( '     <caption>バージョン一覧</caption>%s', "\n" );
    $html .= sprintf( '     <thead>%s', "\n" );
    $html .= sprintf( '      <tr><td>バージョン</td><td>サイズ</td><td>更新時間</td></tr>%s', "\n" );
    $html .= sprintf( '     </thead>%s', "\n" );
    foreach( @version )
    {
      my $file = $dir . '/' . $_ . '.zip';
      my @stat = stat( $file );
      my @time = localtime( $stat[ 9 ] );
      my $size = &Size( $stat[7] );
      my $time = sprintf( '%d/%02d/%02d %02d:%02d:%02d',
                           $time[5] + 1900, $time[4] + 1, $time[3],
                           $time[2], $time[1], $time[0] );
      $html .= sprintf( '     <tr><td><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>%s',
                        $file, $_ . '.zip', $size, $time, "\n" );
    }
    $html .= sprintf( '    </table>%s', "\n" );
    $html .= sprintf( '   </div>%s', "\n" );
  }
  return $html;
}

sub Size( $ )
{
  my( $s ) = @_;
  my $k = 'B';

  if( $s < 1024 )
  {
  }elsif( $s < 1024 * 1024 )
  {
    #1M以内
    $s /= 1024;
    $k = 'KB';
  }else #elsif( $s < 1024 * 1024 * 1024 )
  {
    #1G以内
    $s /= 1024 * 1024;
    $k = 'MB';
  }

  return sprintf( '%.3f%s', $s, $k );
}

sub HtmlMain()
{
  my $html = '';
  return $html;
}

sub HtmlGameList()
{
  my $html = '';
  opendir( DIR, $GAMEDIR );
  my @dirs = readdir( DIR );
  closedir( DIR );

  my @gamelist;
  foreach( @dirs )
  {
    #unless( $_ =~ /[^\d]/ )
    if ( $_ =~ /^([0-9]+)(_.+){0,1}/ )
    {
      push( @gamelist, $_ );
    }
  }
#$html .= $GAMEDIR . join( ',', @dirs );
  @gamelist = sort{ &GetNum( $b ) <=> &GetNum( $a ) } @gamelist;

  $html .= sprintf( '   <div class="gamelist">' );
  $html .= sprintf( '    <table>' );
  $html .= sprintf( '     <caption>ゲーム一覧</caption>%s', "\n" );
  $html .= sprintf( '     <colgroup class="left"></colgroup>%s', "\n" );
  $html .= sprintf( '     <colgroup span="3" class="center"></colgroup>%s', "\n" );
  $html .= sprintf( '     <colgroup span="2" class="right"></colgroup>%s', "\n" );
  $html .= sprintf( '     <thead>%s', "\n" );
  $html .= sprintf( '      <tr><td>No</td><td>タイトル</td><td>一言</td><td>更新日時</td><td>編集</td><td>削除</td></tr>%s', "\n" );
  $html .= sprintf( '     </thead>%s', "\n" );
  foreach( @gamelist )
  {
    my %data = &GetGameSetting( $_ );

    $_ =~ /([0-9]+)/;
    my $gamenum = $1;

    $html .= sprintf( '     <tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td><a href="%s?number=%d">編集</a></td><td>削除</td></tr>%s',
                      $gamenum, $data{ 'title' }, $data{ 'text' }, &DateSplit( $data{ 'date' } ), $CgiScript, $gamenum, "\n" );
  }
  $html .= sprintf( '    </table>%s', "\n" );
  $html .= sprintf( '   </div>%s', "\n" );

  return $html;
}

sub GetNum()
{
  $_[ 0 ] =~ /([0-9]+)/;
  return $1;
}

sub DateSplit()
{
  $_[ 0 ] =~ /([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})/;
  my ( $year, $month, $day, $hour, $min, $sec ) = ( $1, $2, $3, $4, $5, $6 );
  return sprintf ( '%04d/%02d/%02d %02d:%02d:%02d', $year, $month, $day, $hour, $min, $sec );
}

sub SearchGameDir()
{
  my ( $gamenum ) = ( @_, -1 );

  my $gamedir = '';

  if ( opendir ( DIR, $GAMEDIR ) )
  {
    my @list = readdir ( DIR );
    closedir ( DIR );
    foreach ( @list )
    {
      if ( $_ =~ /([0-9]+)/ )
      {
        my $num = int ( $1 );
        if ( $num == $gamenum ){ $gamedir = $_; last; }
      }
    }
  }

  return $gamedir;
}

sub GetGameSetting()
{
  my ( $gamedir ) = @_;
  $gamedir =~ /([\d]+)/;
  my $gamenum = $1;
#  my $file = sprintf( '%s/%04d/%s', $GAMEDIR, $gamenum, $SETTING );
  my $file = sprintf( '%s/%s/%s', $GAMEDIR, $gamedir, $SETTING );

  unless ( -f $file )
  {
    $file = sprintf( '%s/%s/%s', $GAMEDIR, &SearchGameDir ( $gamenum ), $SETTING );
  }

  open( FILE, "<$file" );
  my @data = <FILE>;
  close( FILE );
  @data = split( /\n+/, join( '', @data ) );

  my %data;
  $data{ 'title' } = $data{ 'text' } = '';
  $data{ 'date' } = $data{ 'dvd' } = $data{ 'pad2key' } = $data{ 'ver' } = 0;
  $data{ 'imagenum' } = 1;
  $data{ 'cate' } = '';

  foreach( @data )
  {
    my( $name, $value ) = split( /=/, $_ );
    $data{ $name } = $value;
  }

  return %data;
}

#ver指定を必要とするように書き換え。
sub DirPath( $ )
{
  my( $num, $idname, $aver ) = ( @_, '', '' );
  my $ver = 0;

  $idname =~ s/[\r\n]//g;
open(F,">path.txt");
print F "1] ($idname) \n";
close(F);
  if ( $aver ne '' && $aver > 0  ){ $ver = int ( $aver ); }

  if ( $idname ne '' ){ $idname = '_' . $idname; }

  if( $num == -1 )
  {
    #新規
    opendir( DIR, "$GAMEDIR" );
    my @gamedir = readdir( DIR );
    closedir( DIR );

    foreach( @gamedir )
    {
      #unless( $_ =~ /[^\d]/ )
      if ( $_ =~ /^([\d]+)(\_.+){0,1}/ )
      {
        my $gnum = $1;
        if( $gnum > $num ){ $num = $gnum; }
      }
    }
    ++$num;
  }

  my $path = $GAMEDIR;
  unless( -d $path )
  {
    mkdir( $path, 0755 );
  }

  $path = sprintf( '%s/%d%s', $path, $num, $idname );
  unless( -d $path )
  {
    mkdir( $path, 0755 );
  }
open(F,">>path.txt");
print F "2] ($path) \n";
close(F);
  $path = sprintf( '%s/%d', $path, $ver );

  unless( -d $path )
  {
    mkdir( $path, 0755 );
  }
open(F,">>path.txt");
print F "3] ($path) \n";
close(F);
  return $path;
}

sub Upload()
{
  my $ret = '';
  my %data;
  my $ver = 0;
  my $gver = 0;
  my $flag = 0;
  my $file = $GAMEDIR . '/' . &SearchGameDir( $cgi{ 'number' } ) . '/' . $SETTING;
open(F,">upload.txt");
print F "1] ($file)\n";
close(F);
  $data{ 'first' } = 0;
  if ( -f $file )
  {
open(F,">>upload.txt");
print F "2] ()\n";
close(F);
    # バージョンアップ
    if ( open ( FILE, "< $file" ) )
    {
      my @line = <FILE>;
      close ( FILE );

      foreach ( @line )
      {
        my ( $key, $value ) = split ( /\=/, $_, 2 );
        #chomp ( $value );#改行コードによっては不発になる
        $value =~ s/[\r\n]+\z//;#どの改行コードでもOKのはず
        if ( $key eq 'cate' )
        {
          push ( @{ $data{ $key } }, split( /,/, $value ) );
        } else
        {
          $data{ $key } = $value;
        }
      }

      $ver = $data{ 'ver' };
      $gver = $data{ 'gver' };
      if( $cgi{ 'file' } =~ /(\.zip)$/i )
      {
        $flag = 2;
        ++$ver;
        ++$gver;
      }
      elsif ( $data{ 'exe' } ne $cgi{ 'exe' } ||
           $data{ 'title' } ne $cgi{ 'title' } ||
           $data{ 'text' } ne $cgi{ 'text' } ||
           $data{ 'imagenum' } != $cgi{ 'imagenum' } ||
           $data{ 'dvd' } != $cgi{ 'dvd' } ||
           $data{ 'pad2key' } != $cgi{ 'pad2key' } ||
           join ( '', @{ $data{ 'cate' } } ) != join ( '', @{ $cgi{ 'category' } } )
         )
      {
        $flag = 1;
        ++$ver;
      }
    }
open(F,">>upload.txt");
print F "2.1] ($ver,$flag)\n";
close(F);
  } else
  {
    # 新規
open(F,">>upload.txt");
print F "2] (new)\n";
close(F);
  }

  my $path = &DirPath( $cgi{ 'number' }, $cgi{ 'idname' }, $ver );
  my @pathcut = split( /\//, $path );
  pop( @pathcut );
  my $datafile = join( '/', @pathcut, $SETTING );
  $ret = pop( @pathcut );
  $ret =~ /([0-9]+)/;
  $ret = '?number=' . $1;

  my @dirs = split( /\//, $path );
  pop( @dirs );
  my $tpath = join( '/', @dirs );

  if( $cgi{ 'image' } =~ /(\.png)$/i )
  {
    #スクリーンショットの作成
    &CreateBinFile( $tpath.'/'.$SSFILE, $cgi{ 'image' } );
    #$ret += 2;
    if( $flag <= 0 )
    {
      $flag = 1;
      ++$ver;
    }
  }else
  {
    #スクリーンショットがない場合は画像を追加する
    unless( -f $tpath.'/'.$SSFILE )
    {
      my $img;
      open( BIN, "<$NOIMAGE" );
      binmode( BIN );
      binmode( STDOUT );
      while(<BIN>){ $img .= $_; }
      close( BIN );

      open( BIN, ">$tpath/$SSFILE" );
      binmode( BIN );
      binmode( STDOUT );
      print BIN $img;
      close( BIN );
      if( $flag <= 0 )
      {
        $flag = 1;
        ++$ver;
      }
    }
    #過去のスクリーンショットがある場合はなにもしない
  }

  if( $cgi{ 'file' } =~ /(\.zip)$/i )
  {
    my $file;
    #ZIPファイルの作成
    my $res = &CreateBinFile( $tpath.'/'.$TEMPZIP, $cgi{ 'file' } );
    #$ret += 1;

    if( $flag <= 1 )
    {
      $flag = 2;
    }
open(F,">>upload.txt");
print F "2.5] (" . $cgi{ 'file' } . ",$flag,$res)\n";
close(F);
  }

#  if( $flag > 0 )
open(F,">>upload.txt");
print F "3.0] ($flag)\n";
close(F);
  if ( $flag > 0 )
  {
    &CreateZip( $path, $gver );
  }

  return $ret;
}

sub CreateBinFile( $$ )
{
  my ( $file, $fp ) = @_;
  if ( open( BIN, ">$file" ) )
  {
    binmode( BIN );
    binmode( STDOUT );
#    flock(IMAGE,2);
    while ( <$fp> )
    {
      print BIN $_;
    }
#    flock(IMAGE,8);
    close( BIN );
    return 0;
  }
  return 1;
}

sub CreateZip( $$ )
{
  my ( $path, $gver ) = @_;
  #ZIPファイルの解凍
  my $unzip;
  my @files;
  my $exe = '';

open(F,">outlog.txt");
print F "1] ($path) \n";
close(F);

  $cgi{ 'first' } = 0;

  if( -f $path.'/../'.$TEMPZIP )
  {
    # 新規
open(F,">>outlog.txt");
print F "1.5] aaa\n";
close(F);
    $unzip = Archive::Zip->new( $path.'/../'.$TEMPZIP );

    #ファイル一覧の取得
    @files = $unzip->memberNames();
    #ファイル数
    my $count = 0;

    #ファイルの保存
    foreach( @files )
    {
      $unzip->extractMember( $_, $path.'/'.$_ );
      $_ = $path.'/'.$_;
      if( $exe eq '' && $_ =~ /(\.exe)$/i )
      {
        $exe = $_;
      }
      ++$count;
    }

  }else
  {
    # アップデート
open(F,">>outlog.txt");
print F "1.5] bbb ($path.'/../'.$TEMPZIP)\n";
close(F);
  my @dirs = split( /\//, $path );
  my $tpath = join( '/', @dirs );
  my $num = pop( @dirs );
open(F,">>outlog.txt");
print F "1.5] bbb ($tpath.'/'.($num-1).'.zip')\n";
close(F);
    $unzip = Archive::Zip->new( $tpath.'/'.($num-1).'.zip' );
    #ファイル一覧の取得
    @files = $unzip->memberNames();
    #ZIP圧縮
    my $zip = Archive::Zip->new();
    foreach( @files )
    {
      my @p = split( /\//, $_ );
      shift( @p );
      shift( @p );
      shift( @p );
      my $tp = join( '/', $path, @p );
      #ファイルの解凍
#        $unzip->extractMember( $_, $path.'/'.$_ );
      $unzip->extractMember( $_, $tp );
      if( $exe eq '' && $_ =~ /(\.exe)$/i )
      {
        $exe = $tp;
      }
      $_=$tp;
    }

open(F,">>outlog.txt");
print F "2] $path/$SETTING\n";
print F sprintf( 'exe=%s%stitle=%s%stext=%s%spad2key=%d%scate=%s%s',
                        $exe, "\r\n",
                        $cgi{ 'title'   }, "\r\n",
                        $cgi{ 'text'    }, "\r\n",
                        $cgi{ 'pad2key' }, "\r\n",
                        join( ',', @{ $cgi{ 'category' } } ), "\r\n" );
close(F);


  }


  #/を\に変換
  $exe =~ s/\//\\/g;

  my @dirs = split( /\//, $path );
  my $ver = pop( @dirs );
  my $tpath = join( '/', @dirs );

  #スクリーンショットの追加
  if( -f $tpath.'/'.$SSFILE )
  {
    push( @files, $tpath . '/' . $SSFILE );
  }

  #設定ファイルの作成
  &SaveSettingFile( $tpath . '/' . $SETTING,
                    $exe,
                    $cgi{ 'title'  },
                    $cgi{ 'text'   },
                    $cgi{ 'category' },
                    $cgi{ 'idname' },
                    $cgi{ 'dvd' },
                    $cgi{ 'pad2key' },
                    $cgi{ 'first' },
                    $ver,
                    $gver,
		    $cgi{ 'imagenum' } );

  #設定ファイルの追加
  push( @files, $tpath.'/'.$SETTING );

  #ZIP圧縮
  my $zip = Archive::Zip->new();
  #ファイル登録
  my %files;
  foreach(@files){$files{$_}='';}
  @files = keys( %files );
  foreach( @files )
  {
open(F,">>outlog.txt");
print F "3]+ $_\n";
close(F);
    if( -d $_ )
    {
      #ディレクトリの追加
      my ( $t, $d ) = split( /\//, $_, 2 );
#      $zip->addTree( $_, $d );
    }else
    {
      #ファイルの追加
      $zip->addFile( $_ );
    }
  }
  #ZIPファイル出力
  $zip->writeToFileNamed( $path.'.zip','zip' );
return 0;
  #全ファイル削除
  &Remove( $path.'/' );
  rmdir( $path.'/' );

  return 0;
}

sub SaveSettingFile()
{
  my ( $path, $exe, $title, $text, $cate, $idname, $dvd, $pad2key, $first, $ver, $gver, $imagenum ) = ( @_, '', '', '', '', '', '', '', '', '', '' );
#  if ( $path eq '' || $title eq '' || $text eq '' || $cate eq '' ||
#       $idname eq '' || $pad2key eq '' || $ver eq '' || $imagenum eq '')
#  {
#    return -1;
#  }
  $exe =~ s/[\r\n]//g;
  $idname =~ s/[\r\n]//g;
  my ( $sec, $min, $hour, $day, $month, $year ) = localtime( time() );

  my @cate = ();
  if ( $cate eq '' )
  {
    push ( @cate, scalar ( @CATEGORY ) - 1 );
  } else
  {
    push ( @cate, @{ $cate } );
  }

  my @data;
  push ( @data, sprintf( 'exe=%s', $exe ) );
  push ( @data, sprintf( 'title=%s', $title ) );
  push ( @data, sprintf( 'text=%s', $text ) );
  if ( $first <= 0 )
  {
    push ( @data, sprintf( 'first=%d%02d%02d%02d%02d%02d', $year + 1900, $month + 1, $day, $hour, $min, $sec ) );
  } else
  {
    push ( @data, sprintf( 'first=%d', $first ) );
  }
  push ( @data, sprintf( 'date=%d%02d%02d%02d%02d%02d', $year + 1900, $month + 1, $day, $hour, $min, $sec ) );
  push ( @data, sprintf( 'cate=%s', join( ',', @cate ) ) );
  push ( @data, sprintf( 'idname=%s', $idname ) );
  push ( @data, sprintf( 'pad2key=%d', $pad2key ) );
  push ( @data, sprintf( 'dvd=%d', $dvd ) );
  push ( @data, sprintf( 'ver=%d', $ver ) );
  push ( @data, sprintf( 'gver=%d', $gver ) );
  if( $imagenum <= 0 )
  {
    $imagenum = 1;
  }
  push ( @data, sprintf( 'imagenum=%d', $imagenum ) );

  open( FILE, "> $path" );
  print FILE join( "\r\n", @data );
  close( FILE );

  return 0;
}

sub Remove( $ )
{
  my ( $o ) = @_;
  if( -d $o )
  {
    opendir( DIR, $o );
    my @list = readdir( DIR );
    closedir( DIR );

    foreach( @list )
    {
      my $p = $o . '/' . $_;
      if( -d $p )
      {
        if( $_ ne '.' && $_ ne '..' )
        {
          &Remove( $p );
          rmdir( $p );
        }
      }else
      {
        unlink( $p );
      }
    }
  }
}
