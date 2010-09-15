#include "QScene.h"
#include <QNaub.h>
#include <Pointer.h>
#include <QGraphicsSceneMouseEvent>
#include <Vec.h>
#include <Box2D/Dynamics/b2World.h>

QScene::QScene(b2World *world) : QGraphicsScene() {
    pointer = new Pointer(world, this);
}

void QScene::add(QNaub *qnaub) {
    qnaub->pointer = pointer;
    addItem(qnaub);
}

void QScene::mouseMoveEvent(QGraphicsSceneMouseEvent *event) {
    pointer->setPos(Vec(event->pos()));
    QGraphicsScene::mouseMoveEvent(event);
}