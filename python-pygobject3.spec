%define		module	pygobject

Summary:	Python bindings for GObject library
Name:		python-%{module}3
Version:	3.10.1
Release:	1
License:	LGPL
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.10/%{module}-%{version}.tar.xz
# Source0-md5:	3e47b6ebb15eacbdb3cb0f1e3386f7e9
Patch0:		%{name}-link.patch
URL:		http://www.pygtk.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	glib-gio-devel >= 1:2.38.0
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	python-devel
BuildRequires:	python-pycairo-devel
BuildRequires:	python3-devel
BuildRequires:	python3-pycairo-devel
BuildRequires:	rpm-pythonprov
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for GObject library.

%package -n python3-pygobject3
Summary:	Python 3.x bindings for GObject library
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-pygobject3
Python 3.x bindings for GObject library.

%package -n python3-pygobject3-devel
Summary:	Python bindings for GObject library
Group:		Development/Languages/Python
Requires:	%{name}-common-devel = %{version}-%{release}
Requires:	python3-pygobject3 = %{version}-%{release}
Requires:	python3-devel

%package common-devel
Summary:	Python bindings for GObject library
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description common-devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%package devel
Summary:	Python bindings for GObject library
Group:		Development/Languages/Python
Requires:	%{name}-common-devel = %{version}-%{release}

%description devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%description -n python3-pygobject3-devel
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
mkdir python python3
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd python
../%configure \
	--disable-silent-rules	\
	--with-python=python
%{__make}

cd ../python3
../%configure \
	PYTHON_LIBS=-lpython3	\
	--disable-silent-rules	\
	--with-python=python3
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C python -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/pygobject

%{__make} -C python3 -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/pygobject

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*/{*.la,*/*.la}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*/{*.la,*/*.la}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%post	-n python3-pygobject3 -p /usr/sbin/ldconfig
%postun	-n python3-pygobject3 -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libpyglib-gi-2.0-python.so.0
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python.so.*.*.*

%dir %{py_sitedir}/gi
%attr(755,root,root) %{py_sitedir}/gi/_gi.so
%attr(755,root,root) %{py_sitedir}/gi/_gi_cairo.so
%attr(755,root,root) %{py_sitedir}/gi/_glib/_glib.so
%attr(755,root,root) %{py_sitedir}/gi/_gobject/_gobject.so

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

%files -n python3-pygobject3
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libpyglib-gi-2.0-python3.so.0
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python3.so.*.*.*

%dir %{py3_sitedir}/gi
%attr(755,root,root) %{py3_sitedir}/gi/_gi.*.so
%attr(755,root,root) %{py3_sitedir}/gi/_gi_cairo.*.so
%attr(755,root,root) %{py3_sitedir}/gi/_glib/_glib.*.so
%attr(755,root,root) %{py3_sitedir}/gi/_gobject/_gobject.*.so

%dir %{py3_sitedir}/gi/_glib
%dir %{py3_sitedir}/gi/_gobject
%dir %{py3_sitedir}/gi/overrides
%dir %{py3_sitedir}/gi/repository
%dir %{py3_sitedir}/pygtkcompat
%{py3_sitedir}/gi/*.py
%{py3_sitedir}/gi/__pycache__
%{py3_sitedir}/gi/_glib/*.py
%{py3_sitedir}/gi/_glib/__pycache__
%{py3_sitedir}/gi/_gobject/*.py
%{py3_sitedir}/gi/_gobject/__pycache__
%{py3_sitedir}/gi/overrides/*.py
%{py3_sitedir}/gi/overrides/__pycache__
%{py3_sitedir}/gi/repository/*.py*
%{py3_sitedir}/gi/repository/__pycache__
%{py3_sitedir}/pygtkcompat/*.py
%{py3_sitedir}/pygtkcompat/__pycache__

%files common-devel
%defattr(644,root,root,755)
%{_includedir}/pygobject-3.0
%{_pkgconfigdir}/pygobject-3.0.pc

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python.so

%files -n python3-pygobject3-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyglib-gi-2.0-python3.so

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{module}
%endif

