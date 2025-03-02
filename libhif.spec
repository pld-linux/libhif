#
# Conditional build:
%bcond_with	rpm5	# build with rpm5

Summary:	Simple package library built on top of hawkey and librepo
Summary(pl.UTF-8):	Prosta biblioteka obsługi pakietów oparta na bibliotekach hawkey i librepo
Name:		libhif
Version:	0.2.3
Release:	4
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
# Source0-md5:	3d97ff8d601a5f67184d6aa11a9296d2
Patch0:		%{name}-rpm5.patch
Patch1:		%{name}-rpm4.19.patch
URL:		https://github.com/hughsie/libhif
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 0.9.8
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	hawkey-devel >= 0.5.3
BuildRequires:	librepo-devel >= 1.7.11
BuildRequires:	libsolv-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.36.0
Requires:	hawkey >= 0.5.3
Requires:	librepo >= 1.7.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides a simple interface to hawkey and librepo and is
currently used by PackageKit and rpm-ostree.

%description -l pl.UTF-8
Ta biblioteka udostępnia prosty interfejs do bibliotek hawkey i
librepo, jest obecnie używana przez pakiety PackageKit i rpm-ostree.

%package devel
Summary:	Header files for libhif library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libhif
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0
Requires:	hawkey-devel >= 0.5.3
Requires:	librepo-devel >= 1.7.11
Requires:	rpm-devel >= 5

%description devel
Header files for libhif library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libhif.

%package static
Summary:	Static libhif library
Summary(pl.UTF-8):	Statyczna biblioteka libhif
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libhif library.

%description static -l pl.UTF-8
Statyczna biblioteka libhif.

%package apidocs
Summary:	libhif API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libhif
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libhif library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libhif.

%prep
%setup -q
%if %{with rpm5}
%patch -P 0 -p1
%else
%patch -P 1 -p1
%endif

%build
export CFLAGS="%{rpmcflags} -D_GNU_SOURCE"
%configure \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhif.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_libdir}/libhif.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhif.so.1
%{_libdir}/girepository-1.0/Hif-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhif.so
%{_datadir}/gir-1.0/Hif-1.0.gir
%{_includedir}/libhif
%{_pkgconfigdir}/libhif.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhif.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libhif
