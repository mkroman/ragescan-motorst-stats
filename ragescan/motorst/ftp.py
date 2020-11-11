import ftplib
import logging

MOTORST_FTP_HOST = '5.44.137.84'
MOTORST_FTP_USER = 'dmr-ftp-user'
MOTORST_FTP_PASS = 'dmrpassword'

class FTP:
  """Provides a convenient wrapper around the FTP server where DMA publishes their files"""

  def __init__(self):
    """Constructs a new FTP wrapper"""
    self.connected = False
    self.logger = logging.getLogger(__name__)

  def connect(self):
    """Connects to the FTP server.

    This is usually not necessary to do manually - any other method will connect if not already
    connected.
    """
    if not self.connected:
      self.logger.debug(f"Connecting to ftp://{MOTORST_FTP_HOST}")
      self.ftp = ftplib.FTP(MOTORST_FTP_HOST)
      self.logger.debug(f"Logging in as {MOTORST_FTP_USER}")
      self.ftp.login(MOTORST_FTP_USER, MOTORST_FTP_PASS)
      self.connected = True

  def cd(self, path):
    """Sets the current directory"""
    if not self.connected:
      self.connect()

    self.logger.debug(f"Changing directory to {path}")
    self.ftp.cwd(path)

  def ls(self, path=""):
    """Returns a list of files in the given path on the remote server"""
    if not self.connected:
      self.connect()

    return self.ftp.nlst(path)

  def download(self, file_name, callback):
    """Downloads the file with the given file_name and calls the given callback for each block
    downloaded
    """
    if not self.connected:
      self.connect()

    self.logger.debug(f"Downloading file {file_name}")
    self.ftp.retrbinary(f"RETR {file_name}", callback)

