/*
 Separated out into a different js file for ease of use by jschroeder
 */
var providers_large = {
    google: {
        name: 'Google',
        url: 'https://www.google.com/accounts/o8/id'
    },
    launchpad: {
        name: 'Launchpad',
        label: 'Your Launchpad.net username.',
        url: 'https://launchpad.net/~{username}'
    },
    yahoo: {
        name: 'Yahoo',
        url: 'http://yahoo.com/'
    },
    aol: {
        name: 'AOL',
        label: 'Enter your AOL screenname.',
        url: 'http://openid.aol.com/{username}'
    },
    myspace: {
        name: 'MySpace',
        label: 'Enter your MySpace username or email address.',
        url: 'http://{username}.myspace.com'
    },
    /*
    verisign: {
        name: 'Verisign',
        label: 'Your Verisign username',
        url: 'http://{username}.pip.verisignlabs.com/'
    },
    openid: {
        name: 'OpenID',     
        label: 'Enter your OpenID.',
        url: null
    }
    */
};
var providers_small = {
    /*
    myopenid: {
        name: 'MyOpenID',
        label: 'Enter your MyOpenID username.',
        url: 'http://{username}.myopenid.com/'
    },
    */
    livejournal: {
        name: 'LiveJournal',
        label: 'Enter your Livejournal username.',
        url: 'http://{username}.livejournal.com'
    },
    flickr: {
        name: 'Flickr',
        label: 'Enter your Flickr username.',
        url: 'http://flickr.com/{username}/'
    },
    technorati: {
        name: 'Technorati',
        label: 'Enter your Technorati username.',
        url: 'http://technorati.com/people/technorati/{username}/'
    },
    blogger: {
        name: 'Blogger',
        label: 'Your Blogger account',
        url: 'http://{username}.blogspot.com/'
    },
    wordpress: {
        name: 'Wordpress',
        label: 'Enter your Wordpress.com username.',
        url: 'http://{username}.wordpress.com/'
    },

    /*
    vidoop: {
        name: 'Vidoop',
        label: 'Your Vidoop username',
        url: 'http://{username}.myvidoop.com/'
    },
    claimid: {
        name: 'ClaimID',
        label: 'Your ClaimID username',
        url: 'http://claimid.com/{username}'
    }
    */
};
