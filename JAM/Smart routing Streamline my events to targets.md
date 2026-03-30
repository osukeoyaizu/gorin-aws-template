## task1
### eb-register-single-device-ruleのイベントパターン
```
{
  "detail": {
    "registration-type": [{
      "prefix": "single"
    }]
  }
}
```

## task2
### eb-register-bulk-device-ruleのイベントパターン
```
{
  "detail": {
    "registration-type": [{
      "prefix": "bulk"
    }]
  }
}
```

## task3
### eb-register-bulk-device-with-priority-ruleのイベントパターン
```
{
  "detail": {
    "registration-type": [{
      "prefix": "bulk"
    }]
  }
}
```

## task4
### eb-reward-privileged-customer-ruleのイベントパターン
```
{
  "detail": {
    "privileged": [{
      "exists": true
    }]
  }
}
```

## task5
### eb-save-image-ruleのイベントパターン
```
{
  "detail": {
    "image-url": [{
      "prefix": "https"
    }]
  }
}
```
