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
%bcond_with doc
%bcond_with gtk

Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version:	1.17.4
Release:	4
License:	BSD
Group:		System/Libraries
URL:		http://cairographics.org/
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz

Patch0:		cairo-multilib.patch

# https://gitlab.freedesktop.org/cairo/cairo/merge_requests/1
Patch1:		0001-Set-default-LCD-filter-to-FreeType-s-default.patch

# Fix generating PDF font names
# https://gitlab.freedesktop.org/cairo/cairo/-/merge_requests/125
Patch2:		125.patch

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
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(egl)
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

%package -n %{libgobject}
Summary:	Cairo-gobject- multi-platform 2D graphics library
Group:		System/Libraries
Conflicts:	%{_lib}cairo2 < 1.12.8-3

%description -n %{libgobject}
This package contains the shared library for %{name}-gobject.

%package -n %{libscript}
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

%package -n %{lib32gobject}
Summary:	Cairo-gobject- multi-platform 2D graphics library (32-bit)
Group:		System/Libraries

%description -n %{lib32gobject}
This package contains the shared library for %{name}-gobject.

%package -n %{lib32script}
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
%autosetup -p1

export CONFIGURE_TOP="$(pwd)"

# Value "YES", causing graphics and other issues on GTK apps. For now force value "NO". (angry)
export ax_cv_c_float_words_bigendian=no

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

mkdir buildnative
cd buildnative
%configure \
	--enable-xlib \
	--enable-ft \
	--enable-ps \
	--enable-pdf \
	--enable-svg \
	--enable-tee \
	--enable-gobject \
	--enable-gl=no \
	--enable-glesv3=yes \
	--enable-egl=yes \
%if %{with doc}
	--enable-gtk-doc \
%endif
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
%{_libdir}/cairo/
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/html/cairo/

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
