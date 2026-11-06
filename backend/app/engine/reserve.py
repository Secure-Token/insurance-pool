def snapshot(total=100000,committed=0,pending=0):
 available=max(0,total-committed-pending)
 return {"total_funded":total,"committed":committed,"pending":pending,"available":available,"utilization":round((committed+pending)/total,4) if total else 0}
