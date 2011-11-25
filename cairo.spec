%define lib_major	2
%define libname		%mklibname cairo %{lib_major}
%define develname	%mklibname -d cairo

#gw check coverage fails in 1.9.4
%define enable_test 0
%define stable 1
%define build_plf 0
%define build_doc 0
%define enable_xcb 0

%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version:	1.10.2
Release:	7
License:	BSD
Group:		System/Libraries
URL:		http://cairographics.org/
%if %{stable}
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.gz
Source1:	http://cairographics.org/releases/%name-%version.tar.gz.sha1
%else
Source0:	http://cairographics.org/snapshots/%name-%version.tar.gz
Source1:	http://cairographics.org/snapshots/%name-%version.tar.gz.sha1
%endif
# http://bugs.freedesktop.org/show_bug.cgi?id=11838
# http://bugs.freedesktop.org/show_bug.cgi?id=13335
# https://bugs.launchpad.net/ubuntu/+source/cairo/+bug/209256
# http://forums.fedoraforum.org/showthread.php?p=1094309#post1094309
Patch5: cairo-respect-fontconfig.patch

%if %{build_doc}
BuildRequires: gtk-doc
%endif
%if %{enable_test}
BuildRequires: fonts-ttf-bitstream-vera
BuildRequires: pkgconfig(poppler-glib)
BuildRequires: pkgconfig(rsvg-2.0)
%endif
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libspectre)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xrender)
BuildRequires: x11-server-xvfb

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

%package -n %{develname}
Summary:	Development files for Cairo library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files for Cairo library.

%prep
%setup -q
%if %{build_plf}
%patch5 -p1
%endif

%build
%configure2_5x \
	--disable-static \
	--disable-glitz \
	--enable-pdf \
	--enable-ps \
	--enable-tee \
%if %{build_doc}
	--enable-gtk-doc \
%endif
%if %{enable_xcb}
	--enable-xcb 
%endif

%make

%if %{enable_test}
%check
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb -screen 0 1600x1200x24 :$XDISPLAY &
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock)
%endif

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name "*.la" -delete

%files -n %{libname}
%doc COPYING
%{_libdir}/libcairo.so.%{lib_major}*
%{_libdir}/libcairo-gobject.so.%{lib_major}*
%{_libdir}/libcairo-script-interpreter.so.%{lib_major}*

%files -n %{develname}
%doc AUTHORS NEWS README
%doc RELEASING BIBLIOGRAPHY BUGS ChangeLog
%attr(755,root,root) %{_bindir}/cairo-trace
%{_libdir}/cairo/
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/cairo/

