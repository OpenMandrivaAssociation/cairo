# cairo is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 2
%define libname %mklibname cairo %{major}
%define libgobject %mklibname cairo-gobject %{major}
%define libscript %mklibname cairo-script-interpreter %{major}
%define devname %mklibname -d cairo
%define lib32name %mklib32name cairo %{major}
%define lib32gobject %mklib32name cairo-gobject %{major}
%define lib32script %mklib32name cairo-script-interpreter %{major}
%define dev32name %mklib32name -d cairo

#gw check coverage fails in 1.9.4
%bcond_with test
%define stable 1
%define build_plf 0
%bcond_with doc
%bcond_with qt4
%bcond_with gtk

%{?_with_plf: %{expand: %%global build_plf 1}}
%if %{build_plf}
%define distsuffix plf
%endif

Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version:	1.16.0
Release:	6
License:	BSD
Group:		System/Libraries
URL:		http://cairographics.org/
%if %{stable}
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz
%else
Source0:	https://www.cairographics.org/snapshots/cairo-%{version}.tar.xz
%endif
# http://bugs.freedesktop.org/show_bug.cgi?id=11838
# http://bugs.freedesktop.org/show_bug.cgi?id=13335
# https://bugs.launchpad.net/ubuntu/+source/cairo/+bug/209256
# http://forums.fedoraforum.org/showthread.php?p=1094309#post1094309
Patch0:		cairo-respect-fontconfig.patch

# https://bugs.freedesktop.org/show_bug.cgi?id=30910
Patch1:		cairo-1.12.2-rosa-buildfix.patch

Patch3:         cairo-multilib.patch

# https://gitlab.freedesktop.org/cairo/cairo/merge_requests/1
Patch4:         0001-Set-default-LCD-filter-to-FreeType-s-default.patch

# https://gitlab.freedesktop.org/cairo/cairo/merge_requests/5
Patch5:         0001-ft-Use-FT_Done_MM_Var-instead-of-free-when-available.patch

# https://github.com/matthiasclasen/cairo/commit/79ad01724161502e8d9d2bd384ff1f0174e5df6e
Patch6:         cairo-composite_color_glyphs.patch

%if %{with doc}
BuildRequires:	gtk-doc
%endif
%if %{with test}
BuildRequires:	fonts-ttf-bitstream-vera
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(rsvg-2.0)
%endif
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gl)
# (tpg) use GL or GLESv2, can not have both
#BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glib-2.0)
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-2.0)
%endif
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libspectre)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	x11-server-xvfb
BuildRequires:	lzo-devel
%if %{with qt4}
BuildRequires:	qt4-devel
%endif
BuildRequires:	pkgconfig(libudev)
#BuildRequires:	binutils-devel
%if %{with compat32}
BuildRequires:	devel(libudev)
BuildRequires:	devel(liblzo2)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libpixman-1)
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libfontconfig)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libpcre)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libspectre)
BuildRequires:	devel(libpoppler-glib)
%endif

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	Cairo - multi-platform 2D graphics library (32-bit)
Group:		System/Libraries
Requires:	%{lib32script} = %{EVRD}

%description -n %{lib32name}
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

%package -n	%{lib32gobject}
Summary:	Cairo-gobject- multi-platform 2D graphics library (32-bit)
Group:		System/Libraries

%description -n	%{lib32gobject}
This package contains the shared library for %{name}-gobject.

%package -n	%{lib32script}
Summary:	Cairo-script-interpreter - multi-platform 2D graphics library (32-bit)
Group:		System/Libraries

%description -n %{lib32script}
This package contains the shared library for %{name}-script-interpretergobject.

%package -n %{dev32name}
Summary:	Development files for Cairo library
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib32gobject} = %{version}-%{release}
Requires:	%{lib32script} = %{version}-%{release}

%description -n %{dev32name}
Development files for Cairo library.
%endif

%prep
%setup -q
%if %{build_plf}
%patch0 -p1
%endif
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

autoreconf -fi

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--enable-ps \
	--enable-pdf
# (tpg) nuke rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
cd ..
%endif

#ifarch %{x86_64}
#export ax_cv_c_float_words_bigendian=yes
#else
# Value "YES", causing graphics and other issues on GTK apps. For now force value "NO". (angry)
export ax_cv_c_float_words_bigendian=no
#endif

mkdir buildnative
cd buildnative
%configure \
	--disable-static \
	--disable-symbol-lookup \
	--disable-directfb \
	--enable-ft \
	--enable-fc \
	--enable-png \
	--enable-pdf \
	--enable-ps \
	--enable-tee \
	--enable-gl \
	--enable-glx \
	--disable-glesv2 \
	--enable-gobject \
	--enable-xlib \
	--enable-xlib-xrender \
	--enable-drm=no \
	--enable-gallium=no \
%if %{with qt4}
	--enable-qt=auto \
%else
	--enable-qt=no \
%endif
%if %{with doc}
	--enable-gtk-doc \
%endif
	--enable-xcb \
	--enable-xcb-shm \
	--disable-xlib-xcb \
	--enable-egl \
	--enable-pthread=yes

# (tpg) nuke rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool


%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C buildnative


%if %{with test}
%check
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb -screen 0 1600x1200x24 :$XDISPLAY &
export DISPLAY=:$XDISPLAY
make -C buildnative check
kill $(cat /tmp/.X$XDISPLAY-lock)
%endif

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C buildnative

%files -n %{libname}
%{_libdir}/libcairo.so.%{major}*

%files -n %{libgobject}
%{_libdir}/libcairo-gobject.so.%{major}*

%files -n %{libscript}
%{_libdir}/libcairo-script-interpreter.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README
%{_bindir}/cairo-trace
%{_bindir}/cairo-sphinx
%{_libdir}/cairo/
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/cairo/

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libcairo.so.%{major}*

%files -n %{lib32gobject}
%{_prefix}/lib/libcairo-gobject.so.%{major}*

%files -n %{lib32script}
%{_prefix}/lib/libcairo-script-interpreter.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/cairo/
%{_prefix}/lib/lib*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
