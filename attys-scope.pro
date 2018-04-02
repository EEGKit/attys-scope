## Modify these variables:
win32 {
TEMPLATE	= app
CONFIG		+= qt release
HEADERS		= attys-scope.h special.h current.h scopewindow.h gain.h highpass.h lowpass.h bandstop.h channel.h
SOURCES		= attys-scope.cpp special.cpp current.cpp scopewindow.cpp gain.cpp lowpass.cpp bandstop.cpp highpass.cpp channel.cpp
TARGET		= attys-scope
INSTALLS        += target
QT             += widgets
QT += network
INCLUDEPATH     += /iir1
LIBS += \
	-L/iir1/Debug \
    -liir_static \
	-lws2_32 \
	-L../AttysComm/cpp/Debug \
	-lattyscomm_static

RESOURCES     = application.qrc
RC_FILE = attysapp.rc
INCLUDEPATH += ../AttysComm/cpp
}

unix {
TEMPLATE	= app
CONFIG		+= qt release c++11
HEADERS		= attys-scope.h scopewindow.h gain.h highpass.h lowpass.h channel.h special.h current.h bandstop.h 
SOURCES		= attys-scope.cpp scopewindow.cpp gain.cpp lowpass.cpp highpass.cpp channel.cpp special.cpp current.cpp bandstop.cpp 
TARGET		= attys-scope
INSTALLS        += target
LIBS            += -liir -lattyscomm -lbluetooth
QT             	+= widgets
QT 		+= network
target.path     = /usr/local/bin
RESOURCES       = application.qrc
}