# Makefile for source rpm: junit
# $Id$
NAME := junit
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
