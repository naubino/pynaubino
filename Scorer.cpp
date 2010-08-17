#include "Scorer.h"
#include "Naubino.h"
#include "Naub.h"

Scorer::Scorer(Naubino *naubino) :
        QObject(), naubino(naubino) {}

void Scorer::sccFound(QList<Naub *> &scc) {
    foreach (Naub *naub, scc) {
        naubino->deleteNaub(naub);
    }
}
