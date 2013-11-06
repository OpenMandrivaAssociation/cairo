%define major	2
%define libname	%mklibname cairo %{major}
%define libgobject %mklibname cairo-gobject %{major}
%define libscript %mklibname cairo-script-interpreter %{major}
%define devname	%mklibname -d cairo

#gw check coverage fails in 1.9.4
%bcond_with	test
%define stable 1
%define build_plf 0
%bcond_with	doc
%bcond_without	xcb
%ifarch %{ix86} x86_64
%bcond_with	egl
%else
%bcond_without	egl
%endif

%{?_with_plf: %{expand: %%global build_plf 1}}
%if %{build_plf}
%define distsuffix plf
%endif

Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version:	1.12.16
Release:	4
License:	BSD
Group:		System/Libraries
URL:		http://cairographics.org/
%if %{stable}
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz
%else
Source0:	http://cairographics.org/snapshots/%{name}-%{version}.tar.gz
%endif
# http://bugs.freedesktop.org/show_bug.cgi?id=11838
# http://bugs.freedesktop.org/show_bug.cgi?id=13335
# https://bugs.launchpad.net/ubuntu/+source/cairo/+bug/209256
# http://forums.fedoraforum.org/showthread.php?p=1094309#post1094309
Patch0:		cairo-respect-fontconfig.patch

# https://bugs.freedesktop.org/show_bug.cgi?id=30910
Patch1:		cairo-1.12.2-rosa-buildfix.patch

# From Fedora, fix possible crashes:
Patch2:		cairo-1.12.8-0-sized-glyph-xlib.patch
Patch3:		cairo-1.12.8-0-sized-glyph-xcb.patch

%if %{with doc}
BuildRequires:	gtk-doc
%endif
%if %{with test}
BuildRequires:	fonts-ttf-bitstream-vera
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(rsvg-2.0)
%endif
BuildRequires:	pkgconfig(directfb)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gl)
%if %{with egl}
BuildRequires:	pkgconfig(egl)
%endif
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libspectre)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	x11-server-xvfb
#BuildRequires:	binutils-devel

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
This package is in restricted repository because this build has LCD subpixel
hinting enabled which are covered by software patents.
%endif

%package -n %{libname}
Summary:	Cairo - multi-platform 2D graphics library
Group:		System/Libraries
Requires:	%{libscript} = %{EVRD}

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
This package is in restricted repository because this build has LCD subpixel
hinting enabled which are covered by software patents.
%endif

%package -n	%{libgobject}
Summary:	Cairo-gobject- multi-platform 2D graphics library
Group:		System/Libraries
Conflicts:	%{_lib}cairo2 < 1.12.8-3

%description -n	%{libgobject}
This package contains the shared library for %{name}-gobject.

%package -n	%{libscript}
Summary:	Cairo-script-interpreter - multi-platform 2D graphics library
Group:		System/Libraries
Conflicts:	%{_lib}cairo2 < 1.12.8-3

%description -n %{libscript}
This package contains the shared library for %{name}-script-interpretergobject.

%package -n %{devname}
Summary:	Development files for Cairo library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libgobject} = %{version}-%{release}
Requires:	%{libscript} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for Cairo library.

%prep
%setup -q
%if %{build_plf}
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
#global ldflags %{ldflags} -fuse-ld=bfd

autoreconf -fi
%configure2_5x \
	--disable-static \
    --disable-symbol-lookup \
	--enable-ft \
	--enable-fc \
	--enable-png \
	--enable-pdf \
	--enable-ps \
	--enable-tee \
	--enable-directfb \
	--enable-gl \
	--enable-glx \
	--enable-gobject \
	--enable-xlib \
	--enable-xlib-xrender \
%if %{with doc}
	--enable-gtk-doc \
%endif
%if %{with xcb}
	--enable-xcb \
	--enable-xlib-xcb \
	--enable-xcb-shm \
%endif
%if %{with egl}
	--enable-egl \
%else
	--disable-egl \
%endif
	--enable-pthread=yes
        #--disable-drm \
        #--disable-gallium

# (tpg) nuke rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%if %{with test}
%check
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb -screen 0 1600x1200x24 :$XDISPLAY &
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock)
%endif

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libcairo.so.%{major}*

%files -n %{libgobject}
%{_libdir}/libcairo-gobject.so.%{major}*

%files -n %{libscript}
%{_libdir}/libcairo-script-interpreter.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README COPYING
%doc RELEASING BIBLIOGRAPHY BUGS ChangeLog
%{_bindir}/cairo-trace
%{_bindir}/cairo-sphinx
%{_libdir}/cairo/
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/cairo/

