# Makefile for source rpm: lucene
# $Id$
NAME := lucene
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
