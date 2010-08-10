%if %mandriva_branch == Cooker
# Cooker
%define release %mkrel 1
%else
# Old distros
%define subrel 1
%define release %mkrel 0
%endif

%define lib_major       2
%define libname        %mklibname cairo %{lib_major}
%define libnamedev     %mklibname -d cairo
%define libnamestaticdev %mklibname -s -d cairo

%define pixman_version 0.17.6

#gw check coverage fails in 1.9.4
%define enable_test 0
%define stable 0
%define build_plf 0
%define build_doc 1

%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif


Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version:        1.9.14
Release:        %release
License:	BSD
Group:		System/Libraries
%if %stable
Source0:	http://cairographics.org/releases/%name-%version.tar.gz
Source1:	http://cairographics.org/releases/%name-%version.tar.gz.sha1
%else
Source0:	http://cairographics.org/snapshots/%name-%version.tar.gz
Source1:	http://cairographics.org/snapshots/%name-%version.tar.gz.sha1
%endif
# gw patches to handle LCD subpixel hinting
# http://bugs.freedesktop.org/show_bug.cgi?id=10301
Patch4: cairo-04_lcd_filter.dpatch
# http://bugs.freedesktop.org/show_bug.cgi?id=11838
# http://bugs.freedesktop.org/show_bug.cgi?id=13335
# https://bugs.launchpad.net/ubuntu/+source/cairo/+bug/209256
# http://forums.fedoraforum.org/showthread.php?p=1094309#post1094309
Patch5: cairo-respect-fontconfig.patch

URL:		http://cairographics.org/
BuildRequires:  freetype2-devel >= 2.1.10
BuildRequires:  libxext-devel
BuildRequires:  libx11-devel
BuildRequires:	libxrender-devel
BuildRequires:	libfontconfig-devel
%if %enable_test
# needed by tests
BuildRequires: fonts-ttf-bitstream-vera
# only needed for pdf tests
#BuildRequires:	libpango-devel >= 1.13.0
# gw for svg tests
BuildRequires:	librsvg-devel
# gw for ps testing
BuildRequires: libspectre-devel
# gw for pdf testing
BuildRequires: libpoppler-glib-devel
%endif
BuildRequires:  x11-server-xvfb
BuildRequires:  pixman-devel >= %{pixman_version}

BuildRequires:	libpng-devel
%if %build_doc
BuildRequires:  gtk-doc
%endif
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
%if %{build_plf}

This package is in PLF because this build has LCD subpixel hinting enabled
which are covered by software patents.
%endif

%package -n %{libname}
Summary:	Cairo - multi-platform 2D graphics library
Group:		System/Libraries
Provides:	cairo = %{version}-%{release}
Requires:	freetype2 >= 2.1.10
Requires:	%{_lib}pixman-1_0 >= %{pixman_version}

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
%if %{build_plf}

This package is in PLF because this build has LCD subpixel hinting enabled
which are covered by software patents.
%endif

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
%if %build_plf
%patch4 -p1
%patch5 -p1
%endif

#autoreconf -fi

%build
export PTHREAD_LIBS=-lpthread
%configure2_5x \
%if %build_doc
--enable-gtk-doc \
%endif
  --enable-pdf --enable-ps --disable-xcb
%make

%check
%if %{enable_test}
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb -screen 0 1600x1200x24 :$XDISPLAY &
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock)
%endif

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
rm -f %buildroot%_libdir/cairo/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post	-n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun	-n %{libname} -p /sbin/ldconfig
%endif


%files -n %{libname}
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%_libdir/libcairo.so.%{lib_major}*
%_libdir/libcairo-script-interpreter.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(644,root,root,755)
%doc RELEASING BIBLIOGRAPHY BUGS ChangeLog
%attr(755,root,root) %_bindir/cairo-trace
%_libdir/cairo/
%_libdir/lib*.so
%attr(644,root,root) %_libdir/lib*.la
%_includedir/*
%_libdir/pkgconfig/*.pc
%_datadir/gtk-doc/html/cairo/

%files -n %{libnamestaticdev}
%defattr(644,root,root,755)
%_libdir/lib*.a


