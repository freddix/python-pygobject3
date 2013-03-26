%define		module	pygobject

Summary:	Python bindings for GObject library
Name:		python-%{module}3
Version:	3.8.0
Release:	1
License:	LGPL
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/gnome/sources/pygobject/3.8/%{module}-%{version}.tar.xz
# Source0-md5:	5a1dc34c787b4320da032e87412caca4
Patch0:		%{name}-link.patch
URL:		http://www.pygtk.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	glib-gio-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	python-devel
BuildRequires:	python-pycairo-devel
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for GObject library.

%package devel
Summary:	Python bindings for GObject library
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%package apidocs
Summary:	pygobject API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
pygobject API documentation.

%prep
%setup -qn %{module}-%{version}
%patch0 -p1

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--with-python=python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/pygobject

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*/{*.la,*/*.la}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libpyglib-gi-2.0-python.so.0
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python.so.*.*.*

%attr(755,root,root) %{py_sitedir}/gi/_gi.so
%attr(755,root,root) %{py_sitedir}/gi/_gi_cairo.so
%attr(755,root,root) %{py_sitedir}/gi/_glib/_glib.so
%attr(755,root,root) %{py_sitedir}/gi/_gobject/_gobject.so

%dir %{py_sitedir}/gi
%dir %{py_sitedir}/gi/_glib
%dir %{py_sitedir}/gi/_gobject
%dir %{py_sitedir}/gi/overrides
%dir %{py_sitedir}/gi/repository
%{py_sitedir}/gi/*.py[co]
%{py_sitedir}/gi/_glib/*.py[co]
%{py_sitedir}/gi/_gobject/*.py[co]
%{py_sitedir}/gi/overrides/*.py[co]
%{py_sitedir}/gi/repository/*.py[co]

%dir %{py_sitedir}/pygtkcompat
%{py_sitedir}/pygtkcompat/*.py[co]

%files devel
%defattr(644,root,root,755)
%{_includedir}/pygobject-3.0
%{_pkgconfigdir}/pygobject-3.0.pc
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python.so

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{module}
%endif

