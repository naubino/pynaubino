#ifndef NAUBMANAGER_H
#define NAUBMANAGER_H

#include "Prereqs.h"

#include <QObject>

class Naub;

class NaubManager : public QObject {
    Q_OBJECT
signals:
    void added(Naub *naub);
    void removed(Naub *naub);
    void joined(Naub *a, Naub *b);
    void merged(Naub *a, Naub *b);
public slots:
    void add(Naub *naub);
    void remove(Naub *naub);
    void join(Naub *a, Naub *b);
    void merge(Naub *a, Naub *b);
};


#endif // NAUBMANAGER_H

