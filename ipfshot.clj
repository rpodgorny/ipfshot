#!/usr/bin/bb

(ns ipfshot
  (:require [clojure.string :as str])
  (:gen-class))

(defn ipfs-ls [url]
  (let [listing (-> (clojure.java.shell/sh "ipfs" "ls" "--size=false" url)
                    (:out)
                    (clojure.string/split #"\n"))]
    (for [x listing]
       (print "AHOJ" x "\n"))))

(ipfs-ls "/ipns/pkg.pacman.store/arch/x86_64/default/db")