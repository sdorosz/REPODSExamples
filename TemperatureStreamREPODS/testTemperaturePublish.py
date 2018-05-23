import os
import argparse
import six
import txaio
import json
import datetime

from twisted.logger import Logger
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.wamp.exception import ApplicationError
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

import Adafruit_DHT


class ClientSession(ApplicationSession):

    def onConnect(self):
        self.log.info("Client connected")
        self.join(self.config.realm, [u'anonymous'])

    def onChallenge(self, challenge):
        self.log.info("Challenge for method {authmethod} received", authmethod=challenge.method)
        raise Exception("We haven't asked for authentication!")

    def onJoin(self, details):
 
        self.topic='topic.not.set.yet'

        ## SUBSCRIBE to the topic and receive events
        ##
        def received(msg):
            self.log.info("data fro temperature event received: {msg}", msg=msg)

        sub = yield self.subscribe(received, self.topic)

        


    def onLeave(self, details):
        self.log.info('session left: {}'.format(details))
        self.disconnect()

    def onDisconnect(self):
        self.log.info('transport disconnected')
        reactor.stop()

if __name__ == '__main__':

    print ('parse command line parameters')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:8080/ws', help='')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default='realm1', help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    runner.run(ClientSession, auto_reconnect=True)