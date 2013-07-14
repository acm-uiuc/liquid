# retuns the proper class for bootstrap-style alerts

def notif_class(item, tol):
  return "error" if len(item) > tol else "info"

