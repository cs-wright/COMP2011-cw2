import unittest
from datetime import date
from app import app, db
from app.models import User, Post, friendship

class SocialNetworkModelTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #Tests start here
    def test_password_hashing(self):
        testUser = User(name='Joe Blogs', username='JB2040', dob=date.today(), gender='Male')
        testUser.setPassword('secret password')
        self.assertFalse(testUser.validatePassword('lamp'))
        self.assertTrue(testUser.validatePassword('secret password'))


    def test_follow_users(self):
        g = User(name='Geoff bridges', username='geoff112')
        e = User(name='Ed Hill', username='E_Hill12')
        db.session.add(g)
        db.session.add(e)
        db.session.commit()
        self.assertEqual(g.friends, [])

        for user in g.following_user():
            self.assertFalse(user in User)

        g.follow(e)
        self.assertTrue(e in g.friends)
        self.assertFalse(g in e.friends)
        e.follow(g)
        self.assertTrue(g in e.friends)
        
        g.unfollow(e)
        self.assertEqual(g.friends, [])

        self.assertTrue(e in g.following_user())
        e.unfollow(g)
    

    def test_not_following(self):
        d = User(name='Dan Smith', username='Smithy')
        e = User(name='Ed Hill', username='E_Hill12')
        f = User(name='Freddy Door', username='Doorman')
        g = User(name='Geoff bridges', username='geoff112')
        db.session.add(d)
        db.session.add(e)
        db.session.add(f)
        db.session.add(g)
        db.session.commit()

        d.follow(e)

        notFollowingList = d.not_following()

        self.assertEqual(notFollowingList, [d, f, g])


    
    def test_posts(self):
        d = User(name='Dan Smith', username='Smithy')
        e = User(name='Ed Hill', username='E_Hill12')

        db.session.add(d)
        db.session.add(e)
        db.session.commit()

        p1 = Post(content='This is the first post', author_id=d.id)
        p2 = Post(content='This is the second post', author_id=e.id)


        db.session.add(p1)
        db.session.add(p2)

        d.follow(d)
        d.follow(e)

        dFollowing = d.following_posts()

        first = dFollowing.pop()
        second = dFollowing.pop()

        

        self.assertEqual(first['content'], p1.content)
        self.assertEqual(second['content'], p2.content)

        e.follow(d)

        eFollowing = e.following_posts()

        first = eFollowing.pop()

        self.assertEqual(first['content'], p1.content)

        db.session.commit()

if __name__ == '__main__':
    unittest.main(verbosity=2)


