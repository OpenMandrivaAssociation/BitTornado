%define name	BitTornado
%define version 0.3.18
%define release %mkrel 1

Summary:	Tool for copying files from one machine to another
Name:		%name
Version:	%version
Release:	%release
Epoch:		0
URL:		http://bittornado.com/
Source0:	http://download2.bittornado.com/download/%name-%version.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name-48.png
##Patch: BitTornado-0.3.18-wxpython2.6.patch
License:	MIT
Group:		Networking/File transfer
BuildRoot:	%_tmppath/%name-buildroot
BuildARch:	noarch	
BuildRequires:	python-devel
#Requires:	wxpython2.6
Requires:	wxPythonGTK
Conflicts:	bittorrent < 4.1.4
Conflicts:	bittorrent-gui  < 4.1.4
Conflicts:	kdelibs-common <= 3.1.3
Obsoletes:	bittorrent-shadowsclient
Provides:	bittorrent-shadowsclient
Requires(post):desktop-file-utils
Requires(postun):desktop-file-utils

%description
BitTorrent is a tool for copying files from one machine to another.
FTP punishes sites for being popular. Since all uploading is done
from one place, a popular site needs big iron and big bandwidth.
With BitTorrent, clients automatically mirror files they download,
making the publisher's burden almost nothing.

This package contains an experimental version of BitTorrent, which
contains many extra features.

%prep
%setup -q -n %name-CVS
##%patch -p1

%build
python ./setup.py build

%install
%__rm -rf %buildroot
python setup.py install --root=%buildroot

# Icons
%__install -D -m 644 %SOURCE1 %buildroot%_miconsdir/%name.png
%__install -D -m 644 %SOURCE2 %buildroot%_iconsdir/%name.png
%__install -D -m 644 %SOURCE3 %buildroot%_liconsdir/%name.png

# Menu
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/applications/
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=BitTornado
Comment=Download BitTorrent files
Exec=%{_bindir}/btdownloadgui.py
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
MimeType=application/x-bittorrent
Categories=GTK;X-MandrivaLinux-Internet-FileTransfer;Network;FileTransfer;P2P;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}-maketorrent.desktop << EOF

[Desktop Entry]
Name=BitTornado Creator
Comment=Create BitTorrent metadata files
Exec=%{_bindir}/btcompletedirgui.py
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;X-MandrivaLinux-Internet-FileTransfer;Network;FileTransfer;P2P;
EOF


# Mime
%__mkdir_p %buildroot%_datadir/mime-info

cat << EOF > %buildroot%_datadir/mime-info/%name.mime
application/x-bittorrent
	ext: torrent
EOF

%clean
%__rm -rf %buildroot

%files
%defattr(-,root,root)
%doc LICENSE.txt README* docs/*.txt
%_bindir/*
%py_puresitedir/*
%_miconsdir/%name.png
%_iconsdir/%name.png
%_liconsdir/%name.png
%_datadir/mime-info/*
%_datadir/applications/mandriva-*