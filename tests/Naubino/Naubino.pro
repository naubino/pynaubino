include(../tests.pri)

message()
message($$OBJECT_DIR)
message()

QT       += testlib
TARGET = tst_Naubino
CONFIG   += qtestlib console thread
CONFIG   -= app_bundle
SOURCES += tst_Naubino.cpp
