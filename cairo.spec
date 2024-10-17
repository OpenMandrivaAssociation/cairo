# cairo is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global optflags %{optflags} -O3

%define major 2
%define libname %mklibname cairo %{major}
%define libgobject %mklibname cairo-gobject %{major}
%define libscript %mklibname cairo-script-interpreter %{major}
%define devname %mklibname -d cairo
%define lib32name %mklib32name cairo %{major}
%define lib32gobject %mklib32name cairo-gobject %{major}
%define lib32script %mklib32name cairo-script-interpreter %{major}
%define dev32name %mklib32name -d cairo

%bcond_with doc

Summary:	Cairo - multi-platform 2D graphics library
Name:		cairo
Version:	1.18.2
Release:	2
License:	BSD
Group:		System/Libraries
URL:		https://cairographics.org/
Source0:	http://cairographics.org/releases/%{name}-%{version}.tar.xz
Patch0:		cairo-multilib.patch

# https://gitlab.freedesktop.org/cairo/cairo/-/issues/547
Patch3:		cairo-1.17.6-sane-font-defaults.patch
BuildRequires:	meson
%if %{with doc}
BuildRequires:	gtk-doc
%endif
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(pixman-1)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-render)
BuildRequires:	pkgconfig(xcb-shm)
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
BuildRequires:	devel(libpcre2-8)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libpcre)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libpoppler-glib)
BuildRequires:	devel(libgs)
BuildRequires:	devel(liblzo2)
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
# This is for compatibility with 3rd party binary packages, in particular
# cuda-nvpp has a dependency on a package called "cairo" instead of the
# libraries provided by it.
Provides:	cairo = %{EVRD}

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
Requires:	devel(libfontconfig)
Requires:	devel(libfreetype)
Requires:	devel(libglib-2.0)
Requires:	devel(libpng16)
Requires:	devel(liblzo2)
Requires:	devel(libpixman-1)
Requires:	devel(libX11)
Requires:	devel(libxcb)
Requires:	devel(libxcb-render)
Requires:	devel(libxcb-shm)
Requires:	devel(libXext)
Requires:	devel(libXrender)
Requires:	devel(libz)

%description -n %{dev32name}
Development files for Cairo library.
%endif

%prep
%autosetup -p1

%if %{with compat32}
%meson32 \
	-Dzlib=enabled \
	-Dsymbol-lookup=disabled \
	-Dspectre=disabled \
	-Dgtk_doc=false \
	-Dtests=disabled

%ninja_build -C build32
%endif

%meson \
	-Dfreetype=enabled \
	-Dfontconfig=enabled \
	-Dglib=enabled \
%if %{with doc}
	-Dgtk_doc=true \
%endif
	-Dspectre=disabled \
	-Dsymbol-lookup=disabled \
	-Dtee=enabled \
	-Dtests=disabled \
	-Dxcb=enabled \
	-Dxlib=enabled

%meson_build

%build
%if %{with compat32}
%ninja_install -C build32
%endif

%meson_install

%files -n %{libname}
%{_libdir}/libcairo.so.%{major}*

%files -n %{libgobject}
%{_libdir}/libcairo-gobject.so.%{major}*

%files -n %{libscript}
%{_libdir}/libcairo-script-interpreter.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS
%{_bindir}/cairo-trace
%{_libdir}/cairo/
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%if %{with doc}
%doc %{_datadir}/gtk-doc/html/cairo/
%endif

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
