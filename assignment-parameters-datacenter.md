Term Project Parameters
This project is 30% of your overall grade, and is broken into three components:

Ideation - 10% of the total project grade (roughly due end of week 8)
Proposal - 20% of the total project grade (roughly due end of week 11)
Final Report and Presentation - 70% of the project grade. (due last day of classes)
Projects can involve at most two people; each person must submit their own ideation, proposal and project report. In each phase, if you are working with someone else, you must explicitly identify the other party.  I have made exceptions for groups of 3, but they must get permission first, and the expectation is the project is at least 50% more complex than what is expected of others.

More details about specific requirements of each phase will be released later for each phase of the project.

Ideation
The "ideation" phase is like a "pitch" for a specific service or concept. For example, you might say:

I want to build a product reservation service, similar to Uber but for roller skates
I want to build a "deep fake as a service" to automate the process of developing deep-fakes
I want to build a service to score "similar" documents
At  the ideation phase, you will be evaluated on how interesting your idea appears to others (hard to quantify), how realistic it seems to other people in the class and how likely it will be fulfill the requirements of the Proposal and Final Project phases.

Proposal
In the Proposal phase, you will refine your (modified) idea, possibly in collaboration with your team partner. In this phase, you need outline the specific technologies you'll be using to build your service as described below in "Project Goals". The specific criteria on which you've be evaluated include clarity in specifying which software components you'll use, how they will be combined and what platform will be used for deployment, the data sources or test cases you'll have and how you'll define "success".

Final Project
The final project report will include a written component, a git repo (in our class gihub), a presentation (e.g. PPT) and a video demonstration (a short ~5min presentation you prepare on YouTube). 

----

Project Goals
The projects are designed to expand your understanding of datacenter applications and the hardware and software components that make up those applications. Thus, we're less interested in what you do and more in how you do it and what you learn. You project must involve building a service rather than simply using an existing tool such as Hadoop, Spark, etc.. Alternatively, you can use a new tool (e.g. the Spark graph query system, Google's Vertex AI system) in a context where you provide a service.

There are several website with cloud project suggestions ( e.g. https://nevonprojects.com/cloud-computing-projects/Links to an external site.) Some example ideas could include:

 

Develop a  "text analysis service" similar to the service provided by http://machine.ioLinks to an external site. using an open source NLP library ( e.g.  https://elitedatascience.com/python-nlp-librariesLinks to an external site. )
Construct a scalable system for recording and processing some kind of "internet of things" data source. There are many datasets ( e.g.  https://hub.packtpub.com/25-datasets-deep-learning-iot/Links to an external site. ) even if you can't collect "live data"
Implement a service similar to "If This Than That" ( https://ifttt.com/Links to an external site. ) or integrate integrate another service into IFTTT
Prototype a bus pass system ( https://nevonprojects.com/cloud-based-bus-pass-system/Links to an external site. )
Build a system that "fingerprints" music files and constructs a database to identify music samples using something like https://ourcodeworld.com/articles/read/973/creating-your-own-shazam-identify-songs-with-python-through-audio-fingerprinting-in-ubuntu-18-04Links to an external site.
Compare the performance of VM-based and Kubernetes-based implementation of a common or available service
Create a scalable service to automatically OCR documents
Set up your own openstack or cloud environment
Build an interface to ... 

Your project must make use of at least five of the following datacenter software components:

 

Message marshalling / encoding
RPC / API interfaces
Message queues
Databases
Key-Value Stores
Distributed Lock Manager
Virtual Machines, containers or "functions as a service"
Storage services (s3, etc)
Software Defined Networks
This is probably easier than you think. For example, an OCR service may use a REST interface to accept documents, store those documents in S3, record metadata about the documents in a Redis or Cassandra database and use a message queue system to distribute work between "workers".

If you want to do something that doesn't fit this constraint, bring it up in the Pizza discussion about projects. As long as we can clearly determine the learning goals of your project and how we can assess them, we'll try to make it work.

In the proposal phase, you should use your knowledge of classes of components to justify what you're choosing specific technologies; you'll get (hopefully) helpful feedback from others.


Resources
You should try to fit your project into the Google Compute platform or AWS if you have credits.

For students with a longer term research focus, there are two other resources

https://www.chameleoncloud.org/Links to an external site. - an NSF-funded cloud service that lets you access "bare metal" servers and virtualized cloud components for teaching and research. This service lets you "lease" a servers for specific time periods. 
https://cloudlab.us/Links to an external site. is an NSF-funded cloud service that spans several locations. It's designed for people doing research in cloud computing and distributed systems. When using cloudlab, you create "profiles" that allocate machines at different locations and networks to connect them. There are extensive tutorials. You need to contact Dr. Goodman to use this resource.