==============
Architecture
==============

Overview
=========

.. graphviz::

   graph Arch {
    compound=true;
    graph [splines=ortho];
    node [shape=component];

    subgraph cluster_tools {
        node [shape=box];
        templer [label="pysiphae.templer\n(Code Generator)"];
        buildout [label="buildout\n(Environment\nBuilder)"];
        ansible [label="ansible\n(Deployment Tool)"];
        bower [label="bower\n(Javascript\nPkgMgr)"];
        label="CLI Tools"
    }

    subgraph cluster_registries {
        viewplugin [label="View Plugin", shape=box3d];
        authplugin [label="Authentication Plugin", shape=box3d];
        storageplugin [label="Storage Plugin", shape=box3d];
        payloadplugin [label="Payload Plugin", shape=box3d];
        viewplugin -- authplugin [style=invis];
        authplugin -- storageplugin [style=invis];
        storageplugin -- payloadplugin [style=invis];
        color="#000000";
        label="Registries";
    }

    subgraph cluster_proxy {
        proxy [label="node-http-proxy\n(Routing Proxy)"];
        color="black";
        label="Proxy Service";
    }
    subgraph cluster_processmgr {
        procmgr [label="pysiphae.processmgr\n(Process Manager)"];   
        color="black";
        label="Process Execution\nService";
    }
    subgraph cluster_web {
        { rank=same;
            wsgi [label="pysiphae.wsgi\n(Web Application)"];
        }
        { rank=same;
            views [label="pysiphae.views\n(Core Views)"];
            runner [label="pysiphae.runner\n(Process Runner)"];
        }
        pyramid [shape=folder,label="Pyramid\n(Base Framework)"];
        auth [label="repoze.who\n(Authorization)"];
        registry [label="zope.components\n(Component Registry)"];
        storages [label="pysiphae.storages\n(Storage Factories)"];
        color="black";
        label="Web Application\nService";
    }

    browser [shape=ellipse, label="Web Browser"];
    buildout -- browser [ltail=cluster_tools, style=invis];
    browser -- proxy [lhead=cluster_proxy];
    proxy -- wsgi;
    proxy -- procmgr;
    wsgi -- auth;
    auth -- views;
    wsgi -- views;
    runner -- views;
    views -- pyramid;
    runner -- pyramid;
    views -- storages;
    procmgr -- runner;
    registry -- pyramid;
    storages -- pyramid;
    authplugin -- registry [ltail=cluster_registries];
   }

