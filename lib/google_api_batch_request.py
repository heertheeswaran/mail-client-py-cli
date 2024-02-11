class GmailBatchRequest:
  def __init__(self, service, creds, callback) -> None:
    self.service = service
    self.callback = callback
    self.creds = creds
  
  def execute(self, requests: list):
    batch_request = self.service.new_batch_http_request()
    for request in requests:
      batch_request.add(request, callback=self.callback)
    batch_request.execute()
    return batch_request

