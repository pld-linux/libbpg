# TODO
# - dynamic lib
Summary:	A library of functions for manipulating BPG image format files
Name:		libbpg
Version:	0.9.4
Release:	0.1
License:	LGPL v2 and BSD
Group:		Libraries
Source0:	http://bellard.org/bpg/%{name}-%{version}.tar.gz
# Source0-md5:	4d7ed917ce57001d5481b465fe9a1735
URL:		http://bellard.org/bpg/
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BPG (Better Portable Graphics) is a image format whose purpose is to
replace the JPEG image format when quality or file size is an issue.

Its main advantages are:
- High compression ratio. Files are much smaller than JPEG for similar
  quality.
- Supported by most Web browsers with a small Javascript decoder.
- Based on a subset of the HEVC open video compression standard.
- Supports the same chroma formats as JPEG (grayscale, YCbCr 4:2:0,
  4:2:2, 4:4:4) to reduce the losses during the conversion. An alpha
  channel is supported. The RGB, YCgCo and CMYK color spaces are also
  supported.
- Native support of 8 to 14 bits per channel for a higher dynamic
  range.
- Lossless compression is supported.
- Various metadata (such as EXIF, ICC profile, XMP) can be included.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%{__sed} -i -e 's,-Os,$(OPTFLAGS),' Makefile
%{__sed} -i -e 's#LDFLAGS=-g#LDFLAGS=%{rpmldflags}#' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPTFLAGS="%{rpmcflags}" \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}}
install -p bpgdec bpgenc $RPM_BUILD_ROOT%{_bindir}
cp -p bpgenc.h libbpg.h $RPM_BUILD_ROOT%{_includedir}
cp -p libbpg.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc html post.js
%attr(755,root,root) %{_bindir}/bpgdec
%attr(755,root,root) %{_bindir}/bpgenc

%files devel
%defattr(644,root,root,755)
%{_includedir}/bpgenc.h
%{_includedir}/libbpg.h
%{_libdir}/libbpg.a
