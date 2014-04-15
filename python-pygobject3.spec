%define		module	pygobject

Summary:	Python bindings for GObject library
Name:		python-%{module}3
Version:	3.12.1
Release:	1
License:	LGPL
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.12/%{module}-%{version}.tar.xz
# Source0-md5:	8608682f221feaac81adb3f4e40dbef3
URL:		http://www.pygtk.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	glib-gio-devel >= 1:2.40.0
BuildRequires:	gobject-introspection-devel >= 1.40.0
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

%package devel
Summary:	Python bindings for GObject library
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-pygobject3 = %{version}-%{release}
Obsoletes:	%{name}-common-devel
Obsoletes:	python3-pygobject3-devel

%description devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%prep
%setup -qn %{module}-%{version}

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

find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;

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
%dir %{py_sitedir}/gi
%attr(755,root,root) %{py_sitedir}/gi/_gi.so
%attr(755,root,root) %{py_sitedir}/gi/_gi_cairo.so

%dir %{py_sitedir}/gi/_gobject
%dir %{py_sitedir}/gi/overrides
%dir %{py_sitedir}/gi/repository
%{py_sitedir}/gi/*.py[co]
%{py_sitedir}/gi/_gobject/*.py[co]
%{py_sitedir}/gi/overrides/*.py[co]
%{py_sitedir}/gi/repository/*.py[co]

%dir %{py_sitedir}/pygtkcompat
%{py_sitedir}/pygtkcompat/*.py[co]
%{py_sitedir}/pygobject-*-py2*.egg-info

%files -n python3-pygobject3
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{py3_sitedir}/gi
%attr(755,root,root) %{py3_sitedir}/gi/_gi.*.so
%attr(755,root,root) %{py3_sitedir}/gi/_gi_cairo.*.so

%dir %{py3_sitedir}/gi/_gobject
%dir %{py3_sitedir}/gi/overrides
%dir %{py3_sitedir}/gi/repository
%dir %{py3_sitedir}/pygtkcompat
%{py3_sitedir}/gi/*.py
%{py3_sitedir}/gi/__pycache__
%{py3_sitedir}/gi/_gobject/*.py
%{py3_sitedir}/gi/_gobject/__pycache__
%{py3_sitedir}/gi/overrides/*.py
%{py3_sitedir}/gi/overrides/__pycache__
%{py3_sitedir}/gi/repository/*.py*
%{py3_sitedir}/gi/repository/__pycache__
%{py3_sitedir}/pygtkcompat/*.py
%{py3_sitedir}/pygtkcompat/__pycache__
%{py3_sitedir}/pygobject-*-py3*.egg-info

%files devel
%defattr(644,root,root,755)
%{_includedir}/pygobject-3.0
%{_pkgconfigdir}/pygobject-3.0.pc

