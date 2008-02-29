%define lib_major       2
%define libname        %mklibname cairo %{lib_major}
%define libnamedev     %mklibname -d cairo
%define libnamestaticdev %mklibname -s -d cairo


Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version: 1.5.12
Release: %mkrel 1
License:	BSD
Group:		System/Libraries
Source0:	http://cairographics.org/releases/%name-%version.tar.gz
Source1:	http://cairographics.org/releases/%name-%version.tar.gz.sha1

URL:		http://cairographics.org/
BuildRequires:  freetype2-devel >= 2.1.10
BuildRequires:  libxext-devel
BuildRequires:  libx11-devel
BuildRequires:	libxrender-devel
BuildRequires:	libfontconfig-devel
BuildRequires:  x11-server-xvfb
BuildRequires:  pixman-devel >= 0.9.4

BuildRequires:	libpng-devel
# only needed for pdf tests
#BuildRequires:	libpango-devel >= 1.13.0
BuildRequires:  gtk-doc
# needed by tests
BuildRequires: fonts-ttf-bitstream-vera
BuildRoot:	%_tmppath/%name-%version-root

%description
Cairo provides anti-aliased vector-based rendering for X. Paths
consist of line segments and cubic splines and can be rendered at any
width with various join and cap styles. All colors may be specified
with optional translucence (opacity/alpha) and combined using the
extended Porter/Duff compositing algebra as found in the X Render
Extension.

Cairo exports a stateful rendering API similar in spirit to the path
construction, text, and painting operators of PostScript, (with the
significant addition of translucence in the imaging model). When
complete, the API is intended to support the complete imaging model of
PDF 1.4.

Cairo relies on the Xc library for backend rendering. Xc provides an
abstract interface for rendering to multiple target types. As of this
writing, Xc allows Cairo to target X drawables as well as generic
image buffers. Future backends such as PostScript, PDF, and perhaps
OpenGL are currently being planned.

%package -n %{libname}
Summary:	Cairo - multi-platform 2D graphics library
Group:		System/Libraries
Provides:	cairo = %{version}-%{release}
Requires:	freetype2 >= 2.1.10

%description -n %{libname}
Cairo provides anti-aliased vector-based rendering for X. Paths
consist of line segments and cubic splines and can be rendered at any
width with various join and cap styles. All colors may be specified
with optional translucence (opacity/alpha) and combined using the
extended Porter/Duff compositing algebra as found in the X Render
Extension.

Cairo exports a stateful rendering API similar in spirit to the path
construction, text, and painting operators of PostScript, (with the
significant addition of translucence in the imaging model). When
complete, the API is intended to support the complete imaging model of
PDF 1.4.

Cairo relies on the Xc library for backend rendering. Xc provides an
abstract interface for rendering to multiple target types. As of this
writing, Xc allows Cairo to target X drawables as well as generic
image buffers. Future backends such as PostScript, PDF, and perhaps
OpenGL are currently being planned.

%package -n %{libnamedev}
Summary:	Development files for Cairo library
Group:		Development/C
Requires:	%{libname} = %version
Provides:	%{name}-devel = %version-%release
Provides:	lib%{name}-devel = %version-%release
Obsoletes:      %mklibname -d cairo 2
Conflicts:	%{_lib}cairo1-devel

%description -n %{libnamedev}
Development files for Cairo library.

%package -n %{libnamestaticdev}
Summary:	Static Cairo library
Group:		Development/C
Requires:	%{libnamedev} = %version
Provides:	lib%name-static-devel = %version
Obsoletes: %mklibname -s -d cairo 2

%description -n %{libnamestaticdev}
Static Cairo library.


%prep
%setup -q

%build
%configure2_5x --enable-gtk-doc  --disable-glitz --enable-pdf --enable-ps --disable-xcb
%make

%check
#XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
#%{_bindir}/Xvfb :$XDISPLAY &
#export DISPLAY=:$XDISPLAY
#make check
#kill $(cat /tmp/.X$XDISPLAY-lock)

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n %{libname} -p /sbin/ldconfig
%postun	-n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%_libdir/libcairo.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(644,root,root,755)
%doc RELEASING BIBLIOGRAPHY BUGS ChangeLog
%_libdir/lib*.so
%attr(644,root,root) %_libdir/lib*.la
%_includedir/*
%_libdir/pkgconfig/*.pc
%_datadir/gtk-doc/html/cairo/

%files -n %{libnamestaticdev}
%defattr(644,root,root,755)
%_libdir/lib*.a


