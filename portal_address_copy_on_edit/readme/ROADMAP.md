- On a cart containing only services, `website_sale` decides whether to also
  update the delivery partner from whether the address was new *before* the
  copy takes place, so the cart keeps the previous address as its delivery
  partner in that case.
- Every edit creates an address, so a customer correcting a typo twice leaves
  two of them behind. Archiving the superseded address is deliberately left
  out, as whether an address is still wanted is a business decision.
