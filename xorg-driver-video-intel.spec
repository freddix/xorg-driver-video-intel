%define		gitver	%{nil}

Summary:	X.org video driver for Intel integrated graphics chipsets
Name:		xorg-driver-video-intel
Version:	2.99.916
%if "%{gitver}" != "%{nil}"
Release:	0.%{gitver}.1
%else
Release:	1
%endif
License:	MIT
Group:		X11/Applications
%if "%{gitver}" != "%{nil}"
Source0:	http://cgit.freedesktop.org/xorg/driver/xf86-video-intel/snapshot/xf86-video-intel-%{gitver}.tar.gz
# Source0-md5:	7e24551eae0b952f4d795e791e88ebe5
%else
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-intel-%{version}.tar.bz2
# Source0-md5:	7e24551eae0b952f4d795e791e88ebe5
%endif
Patch0:		0001-sna-Use-default-monitor-options-on-the-first-output.patch
URL:		http://xorg.freedesktop.org/
BuildRequires:	Mesa-libGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libdrm-devel
BuildRequires:	libtool
BuildRequires:	pixman-devel
BuildRequires:	pkg-config
BuildRequires:	xcb-util-devel
BuildRequires:	xorg-libXvMC-devel
BuildRequires:	xorg-proto
BuildRequires:	xorg-util-macros
BuildRequires:	xorg-xserver-server-devel
Provides:	xorg-driver-video
Requires:	xorg-xserver-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/xf86-video-intel

%description
X.org video driver for Intel integrated graphics chipsets.

%package backlight-helper
Summary:    Backlight helper forIntel integrated graphics chipsets
Group:	    X11/Applications
Requires:   %{name} = %{version}-%{release}
Requires:   polkit

%description backlight-helper
Utility to modify LCD panel brightness.

%prep
%if "%{gitver}" != "%{nil}"
%setup -qn xf86-video-intel-%{gitver}
%else
%setup -qn xf86-video-intel-%{version}
%endif
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.{la,so}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/*/*.la

install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/X11/xorg.conf.d/20-video-intel.conf <<EOF
#Section "Device"
#    Identifier	"Intel Graphics"
#    Driver	"intel"
#    Option	"AccelMethod"	"sna"
#    #Option	"AccelMethod"	"uxa"
#EndSection
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_bindir}/intel-virtual-output
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/*.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xorg.conf.d/20-video-intel.conf
%{_mandir}/man4/intel.4*
%{_mandir}/man4/intel-virtual-output.4*

%files backlight-helper
%defattr(644,root,root,755)
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/xf86-video-intel-backlight-helper
%{_datadir}/polkit-1/actions/org.x.xf86-video-intel.backlight-helper.policy

