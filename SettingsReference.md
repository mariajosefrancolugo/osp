**ACTIVE\_ENROLLMENT\_STATUSES**

Enrollment status abbreviations which are considered "active" and will be displayed on a student's profile. Works in tandem with `ENROLLMENT_STATUS_CHOICES`.

**ADMIN\_MEDIA\_PREFIX**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#admin-media-prefix).

**ADMINS**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#admins).

**API\_ALLOWED\_HOSTS**

List of IP addresses for hosts allowed to push data to the API.

**API\_KEY**

Authorization key for pushing data to the API. This should be unique to each OSP installation and should be kept a secret.

**AUTH\_LDAP`_*`**

[See django-auth-ldap documentation](http://packages.python.org/django-auth-ldap/).

**CAMPUS\_CHOICES**

List of campuses for your school.

**CAS`_*`**

[See django-cas documentation](http://code.google.com/p/django-cas/).

**CURRENT\_TERM**

The abbreviation of the term that your school is currently in. Works in tandem with `TERM_CHOICES`.

**CURRENT\_YEAR**

The year that your school is currently in.

**DATABASES**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#databases).

**DEBUG**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#debug).

**DEBUG\_USERS**

List of developers who receive email messages while `DEBUG=True`. This is to prevent students and staff from receiving test email messages from OSP.

**EMAIL\_HOST**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#email-host).

**EMAIL\_HOST\_USER**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#email-host-user).

**EMAIL\_HOST\_PASSWORD**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#email-host-password).

**EMAIL\_PORT**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#email-port).

**ENROLLMENT\_STATUS\_CHOICES**

List of all potential enrollment status choices that could be received by the API. This should be a list of two-tuples, with each one listing the abbreviation and the full text, like so: `('N', 'New')`

**INTERVENTIONS\_EMAIL**

Email address that all intervention requests are sent to.

**INTERVENTION\_REASONS**

List of potential reasons displayed to an instructor when they are submitting an intervention for a student.

**LOGIN\_REDIRECT\_URL**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#login-redirect-url).

**LOGIN\_URL**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#login-url).

**LOGOUT\_URL**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#logout-url).

**MANAGERS**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#managers).

**MEDIA\_URL**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#media-url).

**OSP\_EMAIL**

The "From" email address for the application.

**SECRET\_KEY**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#secret-key).

**TERM\_CHOICES**

List of all potential term choices that could be received by the API. This should be a list of two-tuples, with each one listing the abbreviation and the full text, like so: `('sp', 'Spring')`

**TIME\_ZONE**

[See Django documentation](https://docs.djangoproject.com/en/1.2/ref/settings/#time-zone).

**URL\_PREFIX**

A string which is appended to all other URL paths in the settings (`MEDIA_URL`, `ADMIN_MEDIA_PREFIX`, `LOGIN_REDIRECT_URL`, `CAS_REDIRECT_URL`, `LOGIN_URL`, `LOGOUT_URL`).

**VISIT\_CAREER\_SERVICES\_OUTCOME\_CHOICES**

List of potential Career Services outcomes displayed to staff when they are recording a visit for a student.

**VISIT\_CONTACT\_TYPE\_CHOICES**

List of potential contact types displayed to staff when they are recording a visit for a student.

**VISIT\_DEPARTMENT\_CHOICES**

List of departments displayed to staff when they are recording a visit for a student.

**VISIT\_REASON\_CHOICES**

List of potential reasons displayed to staff when they are recording a visit for a student.