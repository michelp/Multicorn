# -*- coding: utf-8 -*-
# Copyright © 2008-2011 Kozea
# This file is part of Multicorn, licensed under a 3-clause BSD license.
from attest import assert_hook
from multicorn.requests import CONTEXT as c

EMPTYTESTS = []
FULLTESTS = []


def emptycorntest(fun):
    EMPTYTESTS.append(fun)
    return fun


def fullcorntest(fun):
    FULLTESTS.append(fun)
    return fun


@emptycorntest
def emptyness(Corn, data):
    """ Tests if the corn is clean """
    # Assert we are on an empty corn :
    corn_len = Corn.all.len()()
    assert corn_len == 0

    items = list(Corn.all())
    assert len(items) == 0


@emptycorntest
def save(Corn, data):
    """ Tests creation of elements """
    length = 0
    for piece in data:
        assert Corn.all.len()() == length
        item = Corn.create(piece)
        assert item.corn is Corn
        item.save()
        length += 1
        assert Corn.all.len()() == length


@fullcorntest
def existence(Corn, data):
    """ Tests the existence of created elements """
    items = list(Corn.all())
    assert len(items) == len(data)

    for piece in data:
        filter = True
        for key in Corn.identity_properties:
            filter &= getattr(c, key) == piece[key]

        item = Corn.all.filter(filter).one()()
        assert item.corn is Corn  # This is an actual Item, not a dict.
        for key, value in item.items():
            assert item[key] == value

        item = Corn.all.filter(filter).one()()
        same_item = Corn.all.filter(filter).one()()
        assert same_item == item
        # The Corn always return new Item instance
        assert same_item is not item


@fullcorntest
def delete(Corn, data):
    """ Tests deleting an element """
    length = Corn.all.len()()

    for item in Corn.all():
        assert Corn.all.len()() == length
        item.delete()
        length -= 1
        assert Corn.all.len()() == length

    assert length == 0
