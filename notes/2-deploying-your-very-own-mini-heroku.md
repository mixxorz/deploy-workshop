# Deploying your very own mini-Heroku

#### Setup

1. Avail of GitHub student pack
2. Create your DigitalOcean account
3. Apply DigitalOcean promo code to get $50 credit

#### Provision your server

Here's where we create our virtual private server on DigitalOcean. Think of it like a virtual machine, but in the cloud, and internet accessible.

**Login to DigitalOcean and create a new droplet**

- Choose Ubuntu 16.0X


- A $5/mo or $10/mo droplet should be fine
- Choose Singapore as your datacenter location since that's pretty close to where we are and that should help with latency.
- Change the hostname to anything. I'll use "workshop" for mine.

After a few minutes, you should now have a running server! You can see the IP address of your server on the DigitalOcean dashboard. DigitalOcean will also email the password for the root user. We'll need this later. For the purposes of this workshop, let's say that the IP address I got is "128.199.212.114".

**SSH into the machine**

To configure the machine, we need to open a terminal on it. To do that, we'll use `ssh`. The command to connect to a server is:

```
$ ssh <user>@<ip>
```

Fresh Linux servers generally start with a user called "root". Let's connect to the server:

```
$ ssh root@128.199.212.114
Warning: Permanently added '128.199.212.114' (ECDSA) to the list of known hosts.
root@128.199.212.114's password:
```

Enter the password that was sent to you. Once you're logged in, it will ask you to change the default password. First enter your current password, then enter your new password twice.

```
You are required to change your password immediately (root enforced)

.
. removed for brevity
.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

Changing password for root.
(current) UNIX password:
Enter new UNIX password:
Retype new UNIX password:
root@workshop:~#
```

Now we have a shell running on the server!

The root user is a special user usually called the "superuser". It has special privileges which lets it access everything. The root user is too powerful for day-to-day use. You might accidentally end up deleting important system files.

To remedy this, we'll create a normal user that we can login with. While still logged in as the root user on your server, run the command `adduser <name>` replacing name with whatever username you want. For this example, I'll use mixxorz.

```
root@workshop:~# adduser mixxorz
Adding user `mixxorz' ...
Adding new group `mixxorz' (1000) ...
Adding new user `mixxorz' (1000) with group `mixxorz' ...
Creating home directory `/home/mixxorz' ...
Copying files from `/etc/skel' ...
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
Changing the user information for mixxorz
Enter the new value, or press ENTER for the default
  Full Name []:
  Room Number []:
  Work Phone []:
  Home Phone []:
  Other []:
Is the information correct? [Y/n] y
root@workshop:~#
```

You'll be asked for a password for your new user. You can also provide additional details if you want, but this is optional.

Next we'll give our new user `sudo` (super user do) privileges so that we don't have to switch user whenever we need root access. Whenever we need root access for a command, we'll just prepend `sudo`. We'll use `sudo` a lot later.

To give a user `sudo` access, we just add the user to the `sudo` group.

```
root@workshop:~# usermod -aG sudo mixxorz
```

Now our user has `sudo` privileges.

Once you're done, you can exit your session by typing `exit`, and we can try and login with our new user.

```
root@workshop:~# exit
logout
Connection to 128.199.212.114 closed.
$ ssh mixxorz@128.199.212.114
mixxorz@128.199.212.114's password:
Welcome to Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-59-generic x86_64)

.
. removed for brevity
.

mixxorz@workshop:~$
```

You're now logged in as your new user.

**Public Key Authentication**

Currently when we log in, we're asked for a password. This is fine, but it'll be more secure if we were using keys instead. Passwords can be brute forced, keys cannot*.

*probably

To use private/public key authentication, we need… a pair of public and private keys. Let's generate a keypair.

> Note: Check your `/Users/<username>/.ssh` folder if you already have an `id_rsa` and `id_rsa.pub` file. If you do, you don't need to generate a new keypair. You can just use that pair.
>
> If you're using a public computer (e.g. the lab computer), it's a good idea to generate a new keypair and copy it to your flash drive or email it to yourself. These files are literally the keys to your server and if you lose them, you'll lose access to your server.

To generate a new keypair, on your local computer, run

```
$ ssh-keygen
```

It will ask you where you want to save your keys and what to call them. The default is `/Users/<username>/.ssh/id_rsa`. The default is preferable, but if you're on a public computer, you might want to save your keys somewhere else. In my case, I'll save my keys in `.ssh/workshop`.

```
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/mixxorz/.ssh/id_rsa): .ssh/workshop
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in .ssh/workshop.
Your public key has been saved in .ssh/workshop.pub.
The key fingerprint is:
SHA256:0qTSONnMq79lftQcXL+jbMizXmEapqYSaDja85W2JhE mixxorz@Earth
The key's randomart image is:
+---[RSA 2048]----+
|                 |
|              .  |
|        .  . . . |
|    EB +    o   .|
|  . *.B S  = +  .|
| o o.+ +  + * .o |
|..o  .* o+..o.. .|
|. o .=.=o .+.+   |
|   oo+=o...o+    |
+----[SHA256]-----+
```

Now we have a new keypair. In my case, the `workshop` file is the private key, and `workshop.pub` is the public key.

If you chose to save it in the default location, then you're done and you can skip to the next section. If you chose to save your keys somewhere else, you need to create or edit the `.ssh/config` file. Open up your text editor and enter the following:

```
Host 128.199.212.114
  IdentityFile "/Users/mixxorz/.ssh/workshop"
```

Save the file `config` in the `.ssh` directory. Make sure you replace the IP address and path to the private key with yours.

**Adding your public key to the server**

For the server to authenticate you with your keys, you need to add the public key to the server. __Login to the server as your user__ and run the following commands:

Create a folder called `.ssh` and update the permissions.

```
mixxorz@workshop:~$ mkdir .ssh
mixxorz@workshop:~$ chmod 700 .ssh
```

Now create a file called `authorized_keys` in the `.ssh` folder. We can use the text editor called `nano`.

```
mixxorz@workshop:~$ nano .ssh/authorized_keys
```

A text editor should open. Copy the contents of your public key (`<key>.pub`) and paste it into `nano`. Then, save the file by typing `Ctrl+X`, then `Y`, then `Enter`. There should now be a file called `authorized_keys` in the `.ssh` directory. We can double check by typing `cat .ssh/authorized_keys`. It should show you your public key.

Now we need to protect this file from being tampered with by updating its permissions.

```
mixxorz@workshop:~$ chmod 600 .ssh/authorized_keys
```

You can now log in to your server using just your keys.

To try it out, exit your SSH session and try to SSH back in. It shouldn't ask you for a password anymore since it's using your keys to authenticate.

**Disabling password authentication**

Now that you can SSH into your server using just your keys, we can disable password authentication altogether for better security.

To disable password authentication, we have to edit the file `/etc/ssh/sshd_config`. This file requires special permissions to edit, so we'll have to use `sudo`.

While logged in to your user, run

```
mixxorz@workshop:~$ sudo nano /etc/ssh/sshd_config
```

With the file open, look for the line `PasswordAuthentication yes`. Chang the value to `no`.

```
PasswordAuthentication no
```

Save the file by typing `Ctrl+X`, `Y`, then `Enter`.

Since we changed the ssh setting, we need to reload the SSH daemon.

```
mixxorz@workshop:~$ sudo systemctl reload ssh
```

> Note: `sudo` only requires you to enter your password the first time. Subsequent use of `sudo` will not prompt you for a password anymore.

It's a good idea to test if you can still log in before you log out. Open a new terminal and try to SSH into your server.

**Setup a basic firewall**

Firewalls prevent outside connections from connecting to our server. For more security, let's set up a basic firewall. The firewall will be using is called UFW, short for UncomplicatedFirewall.

Applications can register profiles with UFW. Let's check what applications are available.

```
mixxorz@workshop:~$ sudo ufw app list
Available applications:
  OpenSSH
```

OpenSSH is the software that allows us to SSH into the server. Without it, we won't be able to SSH into the server. Let's make sure to allow OpenSSH through the firewall. To do that, run

```
mixxorz@workshop:~$ sudo ufw allow OpenSSH
Rules updated
Rules updated (v6)
```

Now let's enable the firewall.

```
mixxorz@workshop:~$ sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
```

If you're still connected, good! If we had turned on the firewall without first allowing OpenSSH through, we would have been disconnected without any way (aside from the DigitalOcean console) of logging in again.

Since we're already configuring the firewall, let's allow a couple more services. Namely HTTP and HTTPS.

```
mixxorz@workshop:~$ sudo ufw allow http
Rule added
Rule added (v6)
mixxorz@workshop:~$ sudo ufw allow https
Rule added
Rule added (v6)
```

Let's check on the status of our firewall.

```
mixxorz@workshop:~$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
80                         ALLOW       Anywhere
443                        ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
80 (v6)                    ALLOW       Anywhere (v6)
443 (v6)                   ALLOW       Anywhere (v6)
```

Here we can see that the firewall is enabled, and the list of all the allowed ports. By default, if the port isn't here, it will be blocked.

**Add a swap file**

The $5 DigitalOcean VPS we created only has 512mb of memory. This is pretty limited even for our basic use case. To extend our mileage a bit, we can add a swap file. A swap file is a file on the disk that acts like extra memory. I won't discuss the theory here, but that's basically it.

For this task, we'll switch to the root user because everything we'll be doing will require root access.

```
mixxorz@workshop:~$ sudo su - root
root@workshop:~#
```

Create the swap file and update the permissions.

```
root@workshop:~# cd /var
root@workshop:/var# touch swap.img
root@workshop:/var# chmod 600 swap.img
```

> `touch` is a program that creates an empty file.

Initialize the swap file.

```
root@workshop:/var# dd if=/dev/zero of=/var/swap.img bs=1024k count=1000
1000+0 records in
1000+0 records out
1048576000 bytes (1.0 GB, 1000 MiB) copied, 3.59986 s, 291 MB/s

root@workshop:/var# mkswap swap.img
Setting up swapspace version 1, size = 1000 MiB (1048571904 bytes)
no label, UUID=4f9d0d7f-8a22-4efe-9300-6682d4521ee2

root@workshop:/var# swapon swap.img
```

What's basically going on here is that `dd` is copying data from `/dev/zero` and putting it into `swap.img`. What's in `/dev/zero`? Literally zeroes. So we're loading 1GB of zeroes into `swap.img`.

`mkswap` then turns `swap.img` into an actual swap file, and `swapon` turns the swap… on.

We can check that it worked by using `free`

```
root@workshop:/var# free
              total        used        free      shared  buff/cache   available
Mem:         500136       41984       12956        4416      445196      425672
Swap:       1023996           0     1023996
```

We can see the "Swap" has a total of ~1GB of free space.

Finally, we need to update `/etc/fstab` to mount our swap at boot.

```
root@workshop:/var# echo "/var/swap.img    none    swap    sw    0    0" >> /etc/fstab
```

The last command appends the string `/var/swap.img    none    swap    sw    0    0` to `/etc/fstab`. 

Your swap should be all setup.

#### Deploying apps to your server

Up until now, we've just been doing basic server maintenance. This is something we'd do every time we set up a new server. Next up we'll install Dokku and actually deploy applications to our server.

**Install dokku**

"The smallest PaaS implementation you've ever seen" is Dokku's tagline. Dokku is a PaaS (Platform as a Service) application that allows us to deploy and manage our web applications. It works almost exactly like Heroku.

Let's install it.

First we'll download the setup script with `wget`.

```
mixxorz@workshop:~$ wget https://raw.githubusercontent.com/dokku/dokku/v0.8.0/bootstrap.sh

.
. removed from brevity
.

2017-01-20 13:04:38 (42.3 MB/s) - ‘bootstrap.sh’ saved [6650/6650]
```

`wget` just downloads files to your server.

Now that we have the setup script, let's run it. This will take about 5 to 10 minutes.

```
mixxorz@workshop:~$ sudo DOKKU_TAG=v0.8.0 bash bootstrap.sh
.
. lots of things
.
. lots and lots of things
.
--> Running post-install dependency installation
```

Once you see that last line, Dokku is now installed!

> Note: If you don't see that line, Dokku might not have been installed properly. Try to run the install script again. It might tell you need to run `sudo dpkg --configure -a`. When it does, do it, then try the install script again.
>
> Once you see the `Running post-install…` line, Dokku is now installed. We just need to reboot our server.
>
> ```
> mixxorz@workshop:~$ sudo reboot
> ```

There's one last setup step before we can use Dokku. Copy the IP address of your server and open it in your web browser. You should see the Dokku Setup page. Copy your public key and paste it in the box, then click "Finish Setup".

We're now ready to deploy our applications on Dokku!

**Deploy your first app**

Like I said earlier, deploying to Dokku is similar to deploying on Heroku. Just to test that everything works, let's push heroku's `node-js-sample` app.

Open a new terminal on our local machine, and let's clone the node-js-sample app.

```
$ git clone https://github.com/heroku/node-js-sample
$ cd node-js-sample/
```

First we need to create our app. You use Dokku like a command line tool through SSH. For example, to create an app, run

```
$ ssh dokku@128.199.212.114 apps:create node-js-sample
Creating node-js-sample... done
```

Simple.

Now let's add a remote to our repo. The address format is `dokku@<ip>:<name-of-app>`.

```
$ git remote add dokku dokku@128.199.212.114:node-js-sample
```

Now we're ready to push our app!

```
$ git push dokku master
Counting objects: 406, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (315/315), done.
Writing objects: 100% (406/406), 214.48 KiB | 0 bytes/s, done.
Total 406 (delta 61), reused 406 (delta 61)
-----> Cleaning up...
-----> Building node-js-sample from herokuish...
-----> Setting config vars
       CURL_CONNECT_TIMEOUT: 5
-----> Setting config vars
       CURL_TIMEOUT: 30
-----> Adding BUILD_ENV to build environment...
-----> Node.js app detected

.
. removed for brevity
.

=====> Application deployed:
       http://128.199.212.114:13971

To dokku@128.199.212.114:node-js-sample
 * [new branch]      master -> master
```

Our app is now deployed!

If you try to access the app through that address (`http://128.199.212.114:13971`), you'll find that you don't get anything. This is because our firewall is blocking that port. Let's allow the port through the firewall. On your server, run

```
mixxorz@workshop:~$ sudo ufw allow 13971
Rule added
Rule added (v6)
```

Now you should see "Hello World!"

**Deploy the public notice board app**

As the last step in this tutorial, let's deploy something more complicated. I made a sample app that we can use to demonstrate how to use and setup backing services in Dokku.

You can find the app here: https://github.com/mixxorz/deploy-workshop (It's also where this post is hosted.)

Since the app requires a postgres database, we need to install postgres on our server. Fortunately, this is only a one liner. On your server, run

```
mixxorz@workshop:~$ sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
-----> Cloning plugin repo https://github.com/dokku/dokku-postgres.git to /var/lib/dokku/plugins/available/postgres
Cloning into 'postgres'...
remote: Counting objects: 858, done.
remote: Total 858 (delta 0), reused 0 (delta 0), pack-reused 858
Receiving objects: 100% (858/858), 175.84 KiB | 151.00 KiB/s, done.
Resolving deltas: 100% (559/559), done.
Checking connectivity... done.
-----> Plugin postgres enabled

.
. removed for brevity
.

Digest: sha256:c95ece3fc06342122fc1e5a2112c5860a4d0c42aeebc313baf57cb3e857d7443
Status: Downloaded newer image for dokkupaas/s3backup:0.5.0-1
latest: Pulling from library/busybox
4b0bc1c4050b: Pull complete
Digest: sha256:817a12c32a39bbe394944ba49de563e085f1d3c5266eb8e9723256bc4448680e
Status: Downloaded newer image for busybox:latest
```

Now if we run `dokku`, we can see we have a new option `postgres`.

```
mixxorz@workshop:~$ dokku
Usage: dokku [--quiet|--trace|--rm-container|--rm|--force] COMMAND <app> [command-specific-options]

.
.
.

Community plugin commands:

    postgres   Plugin for managing Postgres services
```

We'll use this later.

Back on our local machine, let's clone the app.

```
$ git clone https://github.com/mixxorz/deploy-workshop.git
$ cd deploy-workshop/
```

Create the `hello` app on Dokku…

```
$ ssh dokku@128.199.212.114 apps:create hello
Creating hello... done
```

and add the `dokku` remote.

```
$ git remote add dokku dokku@128.199.212.114:hello
```

Next we'll create the database. We'll call it `hello-db`.

```
$ ssh dokku@128.199.212.114 postgres:create hello-db
       Waiting for container to be ready
       Creating container database
       Securing connection to database
=====> Postgres container created: hello-db
=====> Container Information
       Config dir:          /var/lib/dokku/services/postgres/hello-db/config
       Data dir:            /var/lib/dokku/services/postgres/hello-db/data
       Dsn:                 postgres://postgres:370347f64872dafa0afed2d713e77e5f@dokku-postgres-hello-db:5432/hello_db
       Exposed ports:       -
       Id:                  3449e0a52b74b151fd7ef6610192e629b530badf1999ee2963603d03477f621c
       Internal ip:         172.17.0.3
       Links:               -
       Service root:        /var/lib/dokku/services/postgres/hello-db
       Status:              running
       Version:             postgres:9.6.1
```

Next we'll link `hello-db` to our `hello` app

```
$ ssh dokku@128.199.212.114 postgres:link hello-db hello
no config vars for hello
-----> Setting config vars
       DATABASE_URL: postgres://postgres:370347f64872dafa0afed2d713e77e5f@dokku-postgres-hello-db:5432/hello_db
-----> Restarting app hello
App hello has not been deployed
```

Our app now has a linked database.

Before we deploy, let's set the app's required environment variables.

```
$ ssh dokku@128.199.212.114 config:set hello SECRET_KEY=supersecretkey ALLOWED_HOSTS=128.199.212.114
-----> Setting config vars
       SECRET_KEY:    supersecretkey
       ALLOWED_HOSTS: 128.199.212.114
-----> Restarting app hello
App hello has not been deployed
```

Now we're ready to deploy!

```
$ git push dokku master
Counting objects: 71, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (62/62), done.
Writing objects: 100% (71/71), 13.60 KiB | 0 bytes/s, done.
Total 71 (delta 25), reused 0 (delta 0)
-----> Cleaning up...
-----> Building hello from herokuish...
-----> Adding BUILD_ENV to build environment...
-----> Python app detected

.
. removed for brevity
.

=====> Application deployed:
       http://128.199.212.114:64026

To dokku@128.199.212.114:hello
 * [new branch]      master -> master
```

Now that our app is running on the server, we need to migrate the database. Run

```
$ ssh dokku@128.199.212.114 run hello python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, notice_board, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying notice_board.0001_initial... OK
  Applying sessions.0001_initial... OK
```

Finally, let's allow the app's port through the firewall. On the server

```
mixxorz@workshop:~$ sudo ufw allow 64026
```

Now if we visit http://128.199.212.114:64026, we should see our app!

### Conclusion

We spun up a new VPS, did some basic server management, installed Dokku, and deployed some apps. You can now use your server to deploy any app you like!
