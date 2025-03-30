import { useState } from 'react'

import { Card, StyledBody, StyledAction } from "baseui/card";
import { Button } from "baseui/button";
import { Input } from 'baseui/input';
import axios from 'axios';
import { FormControl } from "baseui/form-control";
import { Notification, KIND } from "baseui/notification";
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router';

export const Login = (setLoginCb) => {
  const navigate = useNavigate();
  const [userName, setUserName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>("")
  const [cookies, setCookie, removeCookie] = useCookies();

  const handleLogin = () => {
    axios.post(`http://localhost:5001/api/user/login/`, {
      "email": userName,
      "password": password
    }, { headers: { "Content-Type": "application/json" }, withCredentials: true }
    )
      .then(res => {
        console.log(res.data)
        if (res.data.jwt) {
          setCookie("loggedIn", true);
          setCookie("jwt", res.data.jwt);
          setTimeout(()=>navigate("/"), 2000);
        }
      }).catch(error => {
        console.error(error)
        if (error.response?.data?.message)
          setError(error.response.data.message);
        else
          setError(error.message);
      })
  }


  return (<>
    <Card
      title="Login"
    >
      <StyledBody>
        <FormControl label="User name">
          <Input
            value={userName}
            onChange={e => setUserName(e.target.value)}
            placeholder="JohnDoe"
            clearOnEscape
          />
        </FormControl>
        <FormControl label="Password">

          <Input
            onChange={(event) => setPassword(event.currentTarget.value)}
            type="password"
            value={password}
          />
        </FormControl>

      </StyledBody>
      <StyledAction>
        <Button onClick={handleLogin} overrides={{ BaseButton: { style: { width: "100%" } } }}>
          Login
        </Button>

        <Button onClick={() => navigate("/register")} overrides={{ BaseButton: { style: { width: "100%" } } }}>
          Go to register
        </Button>

        {error && <Notification kind={KIND.negative} closeable>
          {() => error}
        </Notification>}
      </StyledAction>
    </Card>
  </>);
}