#
# Conditional build:
%bcond_without	sdl	# SDL based viewer
%bcond_with	x265	# x265 support in BPG encoder
#
Summary:	A library of functions for manipulating BPG image format files
Summary(pl.UTF-8):	Biblioteka funkcji do operacji na plikach obrazów w formacie BPG
Name:		libbpg
Version:	0.9.5
Release:	1
# The original BPG code is BSD-licensed, while the modified FFmpeg library is under LGPLv2.1.
License:	LGPL v2.1 and BSD
Group:		Libraries
Source0:	http://bellard.org/bpg/%{name}-%{version}.tar.gz
# Source0-md5:	30d1619656955fb3fbba5fe9f9f27f67
Patch0:		%{name}-shared.patch
URL:		http://bellard.org/bpg/
%if %{with sdl}
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
%endif
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
%{?with_x265:BuildRequires:	libx265-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BPG (Better Portable Graphics) is a image format whose purpose is to
replace the JPEG image format when quality or file size is an issue.

Its main advantages are:
- High compression ratio. Files are much smaller than JPEG for similar
  quality.
- Supported by most Web browsers with a small JavaScript decoder.
- Based on a subset of the HEVC open video compression standard.
- Supports the same chroma formats as JPEG (grayscale, YCbCr 4:2:0,
  4:2:2, 4:4:4) to reduce the losses during the conversion. An alpha
  channel is supported. The RGB, YCgCo and CMYK color spaces are also
  supported.
- Native support of 8 to 14 bits per channel for a higher dynamic
  range.
- Lossless compression is supported.
- Various metadata (such as EXIF, ICC profile, XMP) can be included.

%description -l pl.UTF-8
BPG (Better Portable Graphics - lepsza przenośna grafika) to format
obrazu, którego celem jest zastąpienie formatu JPEG tam, gdzie ma
znaczenie jakość lub rozmiar pliku.

Główne zalety to:
- ma wysoki współczynnik kompresji; pliki są znacznie mniejsze niż
  JPEG o podobnej jakości
- jest obsługiwany przez większość przeglądarek WWW przy użyciu małego
  dekodera w JavaScripcie
- jest oparty na podzbiorze otwartego standardu kompresji obrazu HEVC
- obsługuje te same schematy barw, co JPEG (odcienie szarości, YCbCr
  4:2:0, 4:2:2, 4:4:4) w celu ograniczenia strat przy konwersji;
  obsługiwany jest kanał alfa oraz przestrzenie barw RGB, YCgCo i CMYK
- ma natywną obsługę 8 i 14 bitów na kanał w celu zapewnienia większej
  dynamiki
- obsługiwana jest kompresja bezstratna
- można dołączać różne metadane (jak EXIF, profil ICC, XMP).

%package devel
Summary:	Development files for libbpg library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libbpg
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use libbpg.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących libbpg.

%package static
Summary:	Static libbpg library
Summary(pl.UTF-8):	Statyczna biblioteka libbpg
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbpg library.

%description static -l pl.UTF-8
Statyczna biblioteka libbpg.

%package tools
Summary:	Tools to encode and decode BPG files
Summary(pl.UTF-8):	Narzędzia do kodowania i dekodowania plików BPG
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description tools
Tools to encode and decode BPG files.

%description tools -l pl.UTF-8
Narzędzia do kodowania i dekodowania plików BPG.

%package view
Summary:	SDL based BPG images viewer
Summary(pl.UTF-8):	Oparta na SDL przeglądarka obrazów BPG
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description view
SDL based BPG images viewer.

%description view -l pl.UTF-8
Oparta na SDL przeglądarka obrazów BPG.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's,-Os,$(OPTFLAGS),' Makefile
%{__sed} -i -e 's#LDFLAGS=-g#LDFLAGS=%{rpmldflags}#' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPTFLAGS="%{rpmcflags}" \
	%{!?with_sdl:USE_BPGVIEW=} \
	%{?with_x265:USE_X265=y} \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-lib \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} \
	libdir=%{_libdir}

%if %{with sdl}
install bpgview $RPM_BUILD_ROOT%{_bindir}
%endif

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbpg.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README doc/bpg_spec.txt html post.js
%attr(755,root,root) %{_libdir}/libbpg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbpg.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbpg.so
%{_includedir}/bpgenc.h
%{_includedir}/libbpg.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libbpg.a

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bpgdec
%attr(755,root,root) %{_bindir}/bpgenc

%if %{with sdl}
%files view
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bpgview
%endif
