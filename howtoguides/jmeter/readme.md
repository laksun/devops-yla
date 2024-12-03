2.1. Create a JMeter Test Plan and Thread Group
We’ll use the JMeter GUI to set up our Test Plan. First, let’s add a Thread Group to our Test Plan:

2
Further, let’s configure the thread group to use five threads having a ramp-up period of one second with a loop count of 10:

3
Configuring HTTP Request Sampler
Now, let’s create an HTTP Request Sampler within this Thread Group:

4
Let’s configure the HTTP Sampler to use the GET endpoint provided by the Postman echo service:

5
Configuring Summary Report Listener
Finally, let’s add a Summary Report listener to our Thread Group that summarises the results of our test plan:

summary
With this, we have our basic JMeter script ready. Let’s run this in the GUI and take a look at the generated Summary Report:
