%define lib_major       2
%define lib_name        %mklibname cairo %{lib_major}


Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version: 1.4.2
Release: %mkrel 1
License:	BSD
Group:		System/Libraries
Source0:	http://cairographics.org/releases/%name-%version.tar.bz2
# (fc) 1.3.14-4mdv fix bad aliasing
Patch0:		cairo-1.3.14-fixaliasing.patch

URL:		http://cairographics.org/
BuildRequires:  freetype2-devel >= 2.1.10
%if %mdkversion <= 200600
BuildRequires:	XFree86-devel
BuildRequires:  XFree86-Xvfb
%else
BuildRequires:  libxext-devel
BuildRequires:  libx11-devel
BuildRequires:	libxrender-devel
BuildRequires:	libfontconfig-devel
BuildRequires:  x11-server-xvfb
%endif

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

%package -n %{lib_name}
Summary:	Cairo - multi-platform 2D graphics library
Group:		System/Libraries
Provides:	cairo = %{version}-%{release}
Requires:	freetype2 >= 2.1.10

%description -n %{lib_name}
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

%package -n %{lib_name}-devel
Summary:	Development files for Cairo library
Group:		Development/C
Requires:	%{lib_name} = %version
Provides:	%{name}-devel = %version-%release
Provides:	lib%{name}-devel = %version-%release
Conflicts:	%{_lib}cairo1-devel

%description -n %{lib_name}-devel
Development files for Cairo library.

%package -n %{lib_name}-static-devel
Summary:	Static Cairo library
Group:		Development/C
Requires:	%{lib_name}-devel = %version
Provides:	lib%name-static-devel = %version

%description -n %{lib_name}-static-devel
Static Cairo library.


%prep
%setup -q
%patch0 -p1 -b .fixaliasing

%build
%configure2_5x --enable-gtk-doc  --disable-glitz --enable-pdf --enable-ps --disable-xcb
%make

%check
#XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%if %mdkversion <= 200600
#%{_prefix}/X11R6/bin/Xvfb :$XDISPLAY &
%else
#%{_bindir}/Xvfb :$XDISPLAY &
%endif
#export DISPLAY=:$XDISPLAY
#make check
#kill $(cat /tmp/.X$XDISPLAY-lock)

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n %{lib_name} -p /sbin/ldconfig
%postun	-n %{lib_name} -p /sbin/ldconfig


%files -n %{lib_name}
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README TODO
%_libdir/lib*.so.*

%files -n %{lib_name}-devel
%defattr(644,root,root,755)
%_libdir/lib*.so
%attr(644,root,root) %_libdir/lib*.la
%_includedir/*
%_libdir/pkgconfig/*.pc
%_datadir/gtk-doc/html/cairo/

%files -n %{lib_name}-static-devel
%defattr(644,root,root,755)
%_libdir/lib*.a


