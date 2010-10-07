#!/bin/sh

exec java -cp \
  `build-classpath gnu-regexp javahelp2 /SimplyHTML` \
  com.lightdev.app.shtm.App
