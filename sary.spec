#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Suffix array library
Summary(pl.UTF-8):	Biblioteka tablic sufiksowych
Name:		sary
Version:	1.2.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://sary.sourceforge.net/%{name}-%{version}.tar.gz
# Source0-md5:	10b9a803025c5f428014a7f1ff849ecc
Patch0:		%{name}-link.patch
URL:		http://sary.sourceforge.net/
BuildRequires:	glib2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
sary is a suffix array library and tools.
It provides fast full-text search facilities for text files
on the order of 10 to 100 MB using a data structure called
a suffix array. It can also search specific fields in a text
file by assigning index points to those fields. 

#%description -l pl.UTF-8

%package devel
Summary:	Header files for sary library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sary
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel

%description devel
Header files for sary library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sary.

%package static
Summary:	Static sary library
Summary(pl.UTF-8):	Statyczna biblioteka sary
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static sary library.

%description static -l pl.UTF-8
Statyczna biblioteka sary.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf devel-doc
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/docs devel-doc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libsary.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsary.so.10
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%doc devel-doc/*
%{_libdir}/libsary.so
%{_includedir}/sary
%{_includedir}/sary.h
%{_pkgconfigdir}/sary.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsary.a
%endif
