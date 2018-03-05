import os
import json
import logging
import requests

from api.indy.agent import Holder
from api.indy import eventloop

LEDGER_URL = os.environ.get('LEDGER_URL')
if not LEDGER_URL:
    raise Exception('LEDGER_URL must be set.')


class ClaimParser(object):
    """
    Parses a generic claim.
    """
    def __init__(self, claim: str) -> None:
      self.__logger = logging.getLogger(__name__)
      self.__orgData = claim
      self.__parse()

    def __parse(self):
      self.__logger.debug("Parsing claim ...")
      data = json.loads(self.__orgData)
      self.__claim_type = data["claim_type"]
      self.__claim = data["claim_data"]
      self.__issuer_did = data["claim_data"]["issuer_did"]

      # Get schema from ledger
      # Once we upgrade to later version of
      try:
        resp = requests.get('{}/ledger/domain/{}'.format(
            LEDGER_URL,
            self.__claim['schema_seq_no']
        ))
        self.__schema = resp.json()
      except:
        self.__schema = None

        # TEMP WORKAROUND FOR LEDGER ISSUES - schema_version passed by sri-agent
        sver = data.get('schema_version')
        if sver:
          self.__logger.warning("Error loading schema by seq no - trying Holder")
          try:
            async def run():
              async with Holder() as holder:
                schema_json = await holder.get_schema(
                  self.__issuer_did,
                  self.__claim_type,
                  sver
                )
                self.__schema = json.loads(schema_json)
            eventloop.do(run())
          except:
            self.__logger.error("Loading schema from Holder failed")
            self.__schema = None


    def getField(self, field):
      value = None
      try:
        value = self.__claim["claim"][field][0]
      except:
        pass

      return value

    @property
    def schemaName(self) -> str:
        return self.__claim_type

    @property
    def schema(self) -> str:
        return self.__schema

    @property
    def issuerDid(self) -> str:
        return self.__issuer_did

    @property
    def json(self) -> str:
        return json.dumps(self.__claim)
