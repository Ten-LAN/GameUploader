#!/usr/bin/perl --

# This program Encode Shift-JIS !!!!!!!!!!

use strict;
use warnings;
use Archive::Zip;
use CGI;

# Settings

our @CATEGORY       = ( '�A�N�V����', '�V���[�e�B���O', '�X�|�[�c', '���[�X',  '�p�Y��',  '�e�[�u��', '�V�~�����[�V����', '���[���v���C���O', '���l��',    '�~�j�Q�[��', '���̑�' );
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
      # ���������I�I�I
    }

    $html .= &HtmlAdmin();
    $html .= &HtmlGameList();
  }else
  {
    #�A�b�v���[�_�[
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
    <h2>�����́H</h2>
    <p>������Ten-LAN�p�̃Q�[���A�b�v���[�_�[�ł��B</p>
    <p>�����ɃA�b�v�����Ten-LAN GameDownloader�ɂ�Ten-LAN�ɃC���X�g�[�����邱�Ƃ��\�ł��B</p>
    <h2>�g����</h2>
    <h3>�V�K</h3>
    <p>�A�b�v���[�_�[�ɓ����Ă����̏�Ԃ͐V�K�A�b�v���[�h�ƂȂ�܂��B����͋��ʂ����Ă��������B</p>
    <h3>�o�[�W�����A�b�v</h3>
    <p>�A�b�v���[�_�[�����̃Q�[���ꗗ����o�[�W�����A�b�v����Q�[����T���A�ҏW���N���b�N���Ă��������B�Q�[���̌ʃy�[�W�ɍs���܂��B���̌�͋��ʂ̍�ƂƂȂ�܂��B</p>
    <h3>����</h3>
    <p>�Q�[���^�C�g���A�ꌾ�����A�J�e�S���AZIP�ň��k�����Q�[���f�[�^�ꎮ�APNG�`���̃X�N���[���V���b�g����͂��A�A�b�v���[�h���Ă��������B</p>
    <p>PNG�̃X�N���[���V���b�g�͕K�������K�v�ł͂���܂��񂪁A�����`���[�����݂����Ȃ�܂��BPNG�łȂ��ꍇ����͕ۏ؂��܂���B�܂��A�傫������摜�͐���Ƀe�N�X�`���Ƃ��ēǂݍ��߂܂���BSS��3�����x�Ɏ��߁A����ȏ�������K�v�Ȃ�Q�[�����Ń`���[�g���A����p�ӂ��������ǂ��ł��傤�B</p>
    <p>�Q�[�����ƈꌾ�����͕K�����͂��Ă��������B</p>
    <h4>�J�e�S���ɂ���</h4>
    <p>�J�e�S���̓��C���J�e�S���ƃT�u�J�e�S��������܂��B<input type="radio" checked="checked" />�őI�񂾂��̂̓��C���J�e�S���ŁA1�����I�ׂ܂���B�����`���[�ɂ���Ă̓��C���̐F�����Ɏg����ꍇ������܂��B<input type="checkbox" checked="checked" />�őI���������̂̓T�u�J�e�S���ŁA�����I�Ԃ��Ƃ��\�ł��B�J�e�S�������̓��C���T�u�֌W�Ȃ��q�b�g���܂��B</p>
    <h4>�p�b�h�L�[�ϊ�</h4>
    <p>�p�b�h�L�[�ϊ��Ƃ́A�p�b�h�̓��͂��L�[���͂ɕϊ�����@�\��L���ɂ��邩�ǂ����̐ݒ�ł��B�����L���ɂ���ƈȉ��̂悤�ɃQ�[���p�b�h�̃{�^�����L�[�{�[�h���͂ɕϊ�����܂��B���̂��ߌX�̃Q�[���ŃL�[�R���t�B�O�𓋍ڂ�����A�ݒ�������Ԃ��팸�ł��܂�(�������A�i���O���͂������Ȃ��ȂǁA����������������)�B</p>
    <p>�܂��A�����l�ΐ��p�b�h�L�[�ϊ��ƃp�b�h���̗͂��Ή�������ƁA���������������Ȃ�̂ŁA�p�b�h�L�[�ϊ����g�����A���O�Ńp�b�h���͂��������邩�ǂ��炩��I�����Ă��������B</p>
    <div style="text-align: center;"><img src="pad.png" /></div>
    <p>�Ȃ��A���̃L�[�R���t�B�O��Ten-LAN�ɂčs�������̂������I�ɔ��f���܂��BZ�AX�L�[�Ɋ��蓖�ĂĂ���p�b�g�̃{�^����Ten-LAN�ł̌����L�����Z���̃L�[�ƂȂ�̂ŁA�Q�[���̌���Ȃǂ�����ɍ��킹�Ă����ƃ��[�U�[�t�����h���[�ɂȂ�ł��傤�B</p>
    <h3>�A�b�v���[�h�̊m�F</h3>
    <p>�Q�[���̌ʃy�[�W�ł͉ߋ��̃o�[�W�����ꗗ������܂��B�����łǂ̃o�[�W���������A�b�v���[�h����A�T�C�Y�͂����Ȃ̂���������܂��B�_�E�����[�h���Ċm�F���s�����Ƃ��ł��܂����A�f�B���N�g���͍č\�z����Ă��܂��B</p>
    <h2>�ڍ�</h2>
    <h3>�A�b�v���[�h��̍��</h3>
    <p>�A�b�v���[�h���ꂽZIP�͉𓀂���A�ݒ�t�@�C���ƃX�N���[���V���b�g����ꂽ��ŁA�K�؂Ƀf�B���N�g���\�����������ɍĈ��k����܂��B</p>
    <p>�Q�[�����Ƃɕʂ̎��ʔԍ������蓖�Ă��A���̐�p�f�B���N�g�����ɍ��܂ŃA�b�v�����S�Ẵo�[�W�����̃f�[�^���ۑ�����܂��B</p>
    <p>Ten-LAN�{�͈̂�ԐV�����o�[�W�������_�E�����[�h���C���X�g�[�����܂����A�Â��o�[�W�����̃Q�[���͍폜���܂���B�n�C�X�R�A�Ȃǂ�����������ꍇ�͓W����ePC���������Ă��������B</p>
    <p>�Q�[���^�C�g����ꌾ�͍ŐV�̂ݔ��f����A�ߋ��̂��͖̂�������܂��B������ZIP���k����Ă��邽�߁A�ߋ��̃o�[�W�������_�E�����[�h���ĉ𓀂���Ίm�F�ł��܂��B����̓X�N���[���V���b�g�����l�ł��B</p>
    <h3>�ݒ�t�@�C��</h3>
    <p>�Ĉ��k���ꂽZIP��Game/�Q�[���ԍ�/�̉��ɁA�X�N���[���V���b�g�Ɛݒ�t�@�C�����ݒu����܂��B</p>
    <p>ZIP�Ĉ��k�̍ۂɎ��s�t�@�C��(*.exe)���������܂����A���̍ە�������Ƃǂꂪ�I�΂�邩������܂���B</p>
    <p>�A�b�v���[�h��A��p�y�[�W�ɂ�exe�̃p�X���C���\�Ȃ̂ŁA���̂悤�ȏꍇ�ɂ͎蓮�Œ����Ă��������B</p>
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
    <p>Ten-LAN�{�̂ƃQ�[���C���X�g�[���[�ł��B</p>
    <p class="download"><a href="./Ten-LAN.zip">- Download -</a></p>
    <h2>�Q�[�����X�g(JSON)</h2>
    <p>Ten-LAN�ɓǂݍ��܂���JSON�ł��B</p>
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
   <div style="text-align:center;"><div style="font-size:2em;color:red;">WARNING!!</div><p>������l�ȊO�G��Ȃ����ƁI�I</p></div>
   <h1>�V�X�e���Ǘ�</h1>
   <p class="download"><a href="%s?content=admin&sync=1">- �����J�n -</a></p>
   <h1>�Q�[���Ǘ�</h1>
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
    $uploader = '�Q�[���̃A�b�v�f�[�g';
  } else
  {
    $form{ 'title' } = '�V�����Q�[���̖��O(�����̃Q�[���͉��̈ꗗ��)';
    $form{ 'button' } = 'Upload';
    $form{ 'exe' }    = '';
    $uploader = '�V�K�Q�[���A�b�v���[�h';
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
  $html .= sprintf( '      <tr><td>�Q�[���^�C�g��</td><td><input type="text" name="title" value="%s" class="textinput" /></td></tr>%s', $form{ 'title' }, "\n" );
  $html .= sprintf( '      <tr><td>�ꌾ</td><td><input type="text" name="text" value="%s" class="textinput" /></td></tr>%s', $form{ 'text' }, "\n" );
  $html .= sprintf( '      <tr><td>�J�e�S��<div><input type="radio" checked="checked">���C���J�e�S��</div><div><input type="checkbox" checked="checked">�T�u�J�e�S��</div></td><td>' );
  for ( $i = 0 ; $i < scalar( @CATEGORY ) ; ++$i )
  {
    $html .= sprintf( '<div class="cate" style="background-color:%s;"><input type="radio" name="maincate" value="%d"%s /><input type="checkbox" name="subcate" value="%d"%s />%s</div>', $CATEGORY_COLOR[ $i ], $i, $i == $maincate ? ' checked="checked"' : '',$i, $cate[ $i ], $CATEGORY[ $i ] );
  }
  $html .= sprintf( '<div style="clear:both;"></div></td></tr>%s', "\n" );
  $html .= sprintf( '      <tr><td>�Q�[��(ZIP)</td><td><input type="file" name="file" /></td></tr>%s', "\n" );
  $html .= sprintf( '      <tr><td>�X�N���[���V���b�g(PNG)</td><td><input type="file" name="image" /><br><input type="text" name="imagenum" value="%d" />��(���p����)</td></tr>%s', $form{ 'imagenum' }, "\n" );
  if( $cgi{ 'number' } >= 0 )
  {
    $html .= sprintf( '      <tr><td>���s�t�@�C���p�X</td><td><input type="text" name="exe" value="%s" />��������l�ȊO�G��Ȃ�</td></tr>%s', $form{ 'exe' }, "\n" );
    $html .= sprintf( '      <tr><td>���ʖ�</td><td><input type="hidden" name="idname" value="%s" />%s</td></tr>%s', $form{ 'idname' }, $form{ 'idname' }, "\n" );
    $html .= sprintf( '      <tr><td>���J�N�x</td><td>%.4s</tr>%s', $form{ 'first' }, "\n" );
    $html .= sprintf( '      <tr><td>�o�[�W����</td><td>�ݒ�:%d / �Q�[��:%d</td></tr>%s', $form{ 'ver' }, $form{ 'gver' }, "\n" );
  } else
  {
    $html .= sprintf( '      <tr><td>���ʖ�</td><td><input type="text" name="idname" value="%s" /><br />���p�p���̂݁B�ݒ肷��Ə����������B</td></tr>%s', $form{ 'idname' }, "\n" );
  }
  $html .= sprintf( '      <tr><td>DVD���^</td><td><input type="checkbox" name="dvd" value="1" %s /></td></tr>%s', $checked_dvd, "\n" );
  $html .= sprintf( '      <tr><td>�p�b�h�L�[�ϊ��L��</td><td><input type="checkbox" name="pad2key" value="1" %s /></td></tr>%s', $checked, "\n" );
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
    $html .= sprintf( '     <caption>�o�[�W�����ꗗ</caption>%s', "\n" );
    $html .= sprintf( '     <thead>%s', "\n" );
    $html .= sprintf( '      <tr><td>�o�[�W����</td><td>�T�C�Y</td><td>�X�V����</td></tr>%s', "\n" );
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
    #1M�ȓ�
    $s /= 1024;
    $k = 'KB';
  }else #elsif( $s < 1024 * 1024 * 1024 )
  {
    #1G�ȓ�
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
  $html .= sprintf( '     <caption>�Q�[���ꗗ</caption>%s', "\n" );
  $html .= sprintf( '     <colgroup class="left"></colgroup>%s', "\n" );
  $html .= sprintf( '     <colgroup span="3" class="center"></colgroup>%s', "\n" );
  $html .= sprintf( '     <colgroup span="2" class="right"></colgroup>%s', "\n" );
  $html .= sprintf( '     <thead>%s', "\n" );
  $html .= sprintf( '      <tr><td>No</td><td>�^�C�g��</td><td>�ꌾ</td><td>�X�V����</td><td>�ҏW</td><td>�폜</td></tr>%s', "\n" );
  $html .= sprintf( '     </thead>%s', "\n" );
  foreach( @gamelist )
  {
    my %data = &GetGameSetting( $_ );

    $_ =~ /([0-9]+)/;
    my $gamenum = $1;

    $html .= sprintf( '     <tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td><a href="%s?number=%d">�ҏW</a></td><td>�폜</td></tr>%s',
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

#ver�w���K�v�Ƃ���悤�ɏ��������B
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
    #�V�K
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
    # �o�[�W�����A�b�v
    if ( open ( FILE, "< $file" ) )
    {
      my @line = <FILE>;
      close ( FILE );

      foreach ( @line )
      {
        my ( $key, $value ) = split ( /\=/, $_, 2 );
        #chomp ( $value );#���s�R�[�h�ɂ���Ă͕s���ɂȂ�
        $value =~ s/[\r\n]+\z//;#�ǂ̉��s�R�[�h�ł�OK�̂͂�
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
    # �V�K
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
    #�X�N���[���V���b�g�̍쐬
    &CreateBinFile( $tpath.'/'.$SSFILE, $cgi{ 'image' } );
    #$ret += 2;
    if( $flag <= 0 )
    {
      $flag = 1;
      ++$ver;
    }
  }else
  {
    #�X�N���[���V���b�g���Ȃ��ꍇ�͉摜��ǉ�����
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
    #�ߋ��̃X�N���[���V���b�g������ꍇ�͂Ȃɂ����Ȃ�
  }

  if( $cgi{ 'file' } =~ /(\.zip)$/i )
  {
    my $file;
    #ZIP�t�@�C���̍쐬
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
  #ZIP�t�@�C���̉�
  my $unzip;
  my @files;
  my $exe = '';

open(F,">outlog.txt");
print F "1] ($path) \n";
close(F);

  $cgi{ 'first' } = 0;

  if( -f $path.'/../'.$TEMPZIP )
  {
    # �V�K
open(F,">>outlog.txt");
print F "1.5] aaa\n";
close(F);
    $unzip = Archive::Zip->new( $path.'/../'.$TEMPZIP );

    #�t�@�C���ꗗ�̎擾
    @files = $unzip->memberNames();
    #�t�@�C����
    my $count = 0;

    #�t�@�C���̕ۑ�
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
    # �A�b�v�f�[�g
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
    #�t�@�C���ꗗ�̎擾
    @files = $unzip->memberNames();
    #ZIP���k
    my $zip = Archive::Zip->new();
    foreach( @files )
    {
      my @p = split( /\//, $_ );
      shift( @p );
      shift( @p );
      shift( @p );
      my $tp = join( '/', $path, @p );
      #�t�@�C���̉�
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


  #/��\�ɕϊ�
  $exe =~ s/\//\\/g;

  my @dirs = split( /\//, $path );
  my $ver = pop( @dirs );
  my $tpath = join( '/', @dirs );

  #�X�N���[���V���b�g�̒ǉ�
  if( -f $tpath.'/'.$SSFILE )
  {
    push( @files, $tpath . '/' . $SSFILE );
  }

  #�ݒ�t�@�C���̍쐬
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

  #�ݒ�t�@�C���̒ǉ�
  push( @files, $tpath.'/'.$SETTING );

  #ZIP���k
  my $zip = Archive::Zip->new();
  #�t�@�C���o�^
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
      #�f�B���N�g���̒ǉ�
      my ( $t, $d ) = split( /\//, $_, 2 );
#      $zip->addTree( $_, $d );
    }else
    {
      #�t�@�C���̒ǉ�
      $zip->addFile( $_ );
    }
  }
  #ZIP�t�@�C���o��
  $zip->writeToFileNamed( $path.'.zip','zip' );
return 0;
  #�S�t�@�C���폜
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
