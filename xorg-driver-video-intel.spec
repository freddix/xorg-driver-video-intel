%define		gitver	%{nil}

Summary:	X.org video driver for Intel integrated graphics chipsets
Name:		xorg-driver-video-intel
Version:	2.21.0
%if "%{gitver}" != "%{nil}"
Release:	0.%{gitver}.1
%else
Release:	1
%endif
License:	MIT
Group:		X11/Applications
%if "%{gitver}" != "%{nil}"
Source0:	http://cgit.freedesktop.org/xorg/driver/xf86-video-intel/snapshot/xf86-video-intel-%{gitver}.tar.gz
# Source0-md5:	f029cc261fca75b32ba85b9c4189db88
%else
Source0:	http://xorg.freedesktop.org/releases/individual/driver/xf86-video-intel-%{version}.tar.bz2
# Source0-md5:	f029cc261fca75b32ba85b9c4189db88
%endif
Patch0:		%{name}-configure.patch
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

%description
X.org video driver for Intel integrated graphics chipsets.

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
	--disable-static	\
	--enable-kms-only	\
	--enable-sna
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.{la,so}
rm -f $RPM_BUILD_ROOT%{_libdir}/xorg/modules/*/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/*.so
%{_mandir}/man4/intel.4*

